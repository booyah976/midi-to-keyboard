<h1>Midi to Keyboard</h1>
Control computer keyboard keypresses using a midi device. This project was heavily based on <code>https://github.com/xamox/pygame/blob/master/examples/midi.py</code>
<br></br>
<h2>Installation</h2>
<ol>
<li>Clone/download the repo
<li>Install dependecies via<code> pip install -r requirements.txt</code> or <code> pipenv install</code>
<li>Create a <code>convert.txt</code> if it doesn't already exist
</ol>

<h2>Usage</h2>
<ul>
<li>Run <code>python main.py --list</code> to list available midi devices and their respective device ids
<li>Run <code>python main.py --input [device_id] </code> to start the program. When a key is pushed on the piano/midi device, a red outline should appear on the virtual keyboard layout for the same key.
<li>To change keybinds, press the key on the piano/midi device and click on the highlighted area in the virtual layout. Then type the desired key to bind to.
Keybinds are stored in <code>convert.txt</code>.
<li>Do note that keybinds might stay in the pressed down position when multiple (4+) are pressed at the same time.