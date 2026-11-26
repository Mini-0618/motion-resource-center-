"""Render a CVSD standalone component deterministically via Chrome and FFmpeg."""
import argparse, hashlib, json, os, shutil, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

def render(page_file, output, config=None, browser_path=None):
    executable=browser_path or next((x for x in [
        os.getenv('CHROME_BIN'), shutil.which('chromium'), shutil.which('google-chrome'),
        'C:/Program Files/Google/Chrome/Application/chrome.exe',
        'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
    ] if x and Path(x).exists()),None)
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=executable,headless=True)
        page=browser.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        if config:
            page.add_init_script('window.userSettings='+json.dumps(json.loads(Path(config).read_text(encoding='utf-8')),ensure_ascii=True))
        page.goto(Path(page_file).resolve().as_uri())
        page.wait_for_function('window.READY === true')
        width,height,fps,frames=page.evaluate('[CVSD.tokens.canvas.width,CVSD.tokens.canvas.height,FPS,CVSD_FRAMES]')
        page.set_viewport_size({'width':width,'height':height})
        command=['ffmpeg','-v','error','-y','-f','image2pipe','-framerate',str(fps),'-c:v','mjpeg','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
        fingerprints=set()
        with subprocess.Popen(command,stdin=subprocess.PIPE) as ff:
            try:
                for frame in range(frames):
                    page.evaluate('t=>window.render(t)',frame/fps)
                    jpeg=page.screenshot(type='jpeg',quality=94)
                    ff.stdin.write(jpeg)
                    fingerprints.add(hashlib.sha256(jpeg).hexdigest())
            finally:
                ff.stdin.close()
                if ff.wait()!=0:raise RuntimeError('FFmpeg encode failed')
        texts=page.evaluate('window.TEXTS(window.DUR-1/window.FPS)')
        assert texts and not errors, errors
        assert len(fingerprints)>5, 'No meaningful frame variation'
        if not all(x['x1']>x['x0'] and x['x0']>=-1 and x['x1']<=width+1 and x['y0']>=-1 and x['y1']<=height+1 for x in texts):
            raise ValueError(f'Text outside canvas: {texts!r}')
        browser.close()
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(output)]))['streams'][0]
    assert int(probe['nb_read_frames'])==frames and probe['width']==width and probe['height']==height
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True)
    return dict(frames=frames,fps=fps,width=width,height=height,duration_s=frames/fps,distinct_input_frames=len(fingerprints),end_frame_texts=texts,ffprobe=probe,
                chrome=executable or 'Playwright Chromium',codec=probe['codec_name'],decode='FFmpeg full stream PASS',browser_errors=errors)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('page');parser.add_argument('out')
    parser.add_argument('--settings',help='Complete JSON segment, e.g. settings.json')
    parser.add_argument('--browser',help='Path to a Chromium-compatible executable')
    args=parser.parse_args()
    result=render(args.page,args.out,args.settings,args.browser)
    print(json.dumps(result,ensure_ascii=False,indent=2))
