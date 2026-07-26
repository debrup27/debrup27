"""
Rebuilds everything in the profile SVGs except the braille art block.

Every row is padded out to the same column with a dot leader, which means the dot counts are
arithmetic, not something to hand-edit. Run this after changing any label or value:

    python tools/layout.py

The rows today.py rewrites nightly get an id and a matching `length` in svg_overwrite(); that
length is W - len(label) - 3, so changing W or a label here means updating today.py too.
Dev-only, like tools/braille.py - the daily workflow never runs it.
"""
import re

W = 64      # printable columns after the '. ' gutter; every row ends at this column
X = 490     # stats column x, clear of the 440px-wide art at x=15

# bg, foreground, border, key, value, comment, additions, deletions.
# Light gets GitHub's own light-theme syntax colours: the dark palette's #a5d6ff and #ffa657
# land around 1.4:1 on white, which is unreadable.
THEMES = {
    'dark_mode.svg':  ('#161b22', '#c9d1d9', '#30363d', '#ffa657', '#a5d6ff', '#616e7f', '#3fb950', '#f85149'),
    'light_mode.svg': ('#f6f8fa', '#24292f', '#d0d7de', '#953800', '#0550ae', '#6e7781', '#116329', '#cf222e'),
}


def dots(label_len, value_len):
    """The leader that pushes a row's value out to column W."""
    count = W - label_len - 1 - value_len - 2
    assert count >= 1, f'row of {label_len}+{value_len} is too wide for W={W}'
    return ' ' + '.' * count + ' '


def keys(label):
    return '.'.join(f'<tspan class="key">{part}</tspan>' for part in label.split('.'))


def row(y, label, value, ident=None):
    """One 'label ....... value' line. Passing ident makes it a slot today.py rewrites."""
    attr = f' id="{ident}_dots"' if ident else ''
    value_attr = f' id="{ident}"' if ident else ''
    return (f'<tspan x="{X}" y="{y}" class="cc">. </tspan>{keys(label)}:'
            f'<tspan class="cc"{attr}>{dots(len(label), len(value))}</tspan>'
            f'<tspan class="value"{value_attr}>{value}</tspan>')


def rule(y, title):
    return (f'<tspan x="{X}" y="{y}" class="key">{title}</tspan> '
            f'<tspan class="rule">{"-" * (W + 1 - len(title))}</tspan>')


def field(ident, value, length):
    """An inline leader+value pair inside a row that holds several stats."""
    pad = length - len(value)
    leader = ' ' + '.' * pad + ' ' if pad > 2 else {0: '', 1: ' ', 2: '. '}[max(pad, 0)]
    return (f'<tspan class="cc" id="{ident}_dots">{leader}</tspan>'
            f'<tspan class="value" id="{ident}">{value}</tspan>')


LINES = [
    f'<tspan x="{X}" y="45">debrup@sengupta</tspan> <tspan class="rule">{"-" * 50}</tspan>',
    row(75, 'OS', 'Windows 11, iOS 18.5'),
    row(95, 'Uptime', '22 years, 2 months, 9 days', 'age_data'),
    row(115, 'Host', 'Netaji Subhash Engineering College'),
    row(135, 'Kernel', 'Artificial Intelligence and Machine Learning'),
    row(155, 'IDE', 'VSCode 1.100.2, Cursor'),
    row(185, 'Languages.Programming', 'Python, TypeScript, Dart, C++, Solidity'),
    row(205, 'Languages.Computer', 'HTML, CSS, JSON, YAML, LaTeX, Markdown'),
    row(225, 'Languages.Real', 'English, Hindi, Bengali'),
    row(255, 'Hobbies.Software', 'App Dev, Machine Learning, Generative AI'),
    row(275, 'Hobbies.Gaming', 'Valorant, BGMI, Elden Ring, Dark Souls'),
    rule(305, '- Contact'),
    row(335, 'Email.Personal', 'debrupsengupta289@gmail.com'),
    row(355, 'LinkedIn', 'Debrup Sengupta'),
    row(375, 'Discord', 'debisamood'),
    rule(405, '- GitHub Stats'),
    f'<tspan x="{X}" y="435" class="cc">. </tspan><tspan class="key">Repos</tspan>:'
    + field('repo_data', '14', 6)
    + ' {<tspan class="key">Contributed</tspan>:' + field('contrib_data', '28', 4)
    + '} | <tspan class="key">Stars</tspan>:' + field('star_data', '0', 17),
    f'<tspan x="{X}" y="455" class="cc">. </tspan><tspan class="key">Commits</tspan>:'
    + field('commit_data', '309', 26)
    + ' | <tspan class="key">Followers</tspan>:' + field('follower_data', '4', 13),
    f'<tspan x="{X}" y="475" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:'
    + field('loc_data', '255,551', 9)
    + ' ( <tspan id="loc_add_dots"></tspan><tspan class="addColor" id="loc_add">1,507,048</tspan>'
    + '<tspan class="addColor">++</tspan>, '
    + '<tspan id="loc_del_dots"></tspan><tspan class="delColor" id="loc_del">1,251,497</tspan>'
    + '<tspan class="delColor">--</tspan> )',
]

TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="1200" height="510" viewBox="0 0 1200 510" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {key};}}
.value {{fill: {value};}}
.addColor {{fill: {add};}}
.delColor {{fill: {dele};}}
.cc {{fill: {comment};}}
.rule {{fill: url(#accent);}}
.ascii {{font-size: 12px;}}
text, tspan {{white-space: pre;}}
</style>
<defs>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{key}"/>
<stop offset="0.5" stop-color="{value}"/>
<stop offset="1" stop-color="{border}"/>
</linearGradient>
</defs>
<rect x="0.5" y="0.5" width="1199" height="509" fill="{bg}" stroke="{border}" rx="15"/>
{art}

<text x="{x}" y="45" fill="{fg}">
{lines}
</text>
</svg>
"""

if __name__ == '__main__':
    for path, (bg, fg, border, key, value, comment, add, dele) in THEMES.items():
        with open(path, encoding='utf-8') as f:
            art = re.search(r'<text[^>]*class="ascii"[^>]*>.*?</text>', f.read(), re.S).group(0)
        art = re.sub(r'fill="#\w+"', f'fill="{fg}"', art, count=1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(TEMPLATE.format(bg=bg, fg=fg, border=border, key=key, value=value,
                                    comment=comment, add=add, dele=dele,
                                    art=art, x=X, lines='\n'.join(LINES)))
        print('wrote', path)
