"""Build the renamed CompanyText subset from the licensed original font.

Build dependency: fonttools. The original font can also be used directly:
point @font-face to assets/original/LXGWNeoXiHei.ttf with format('truetype').
"""
from pathlib import Path
from fontTools import subset

ROOT=Path(__file__).resolve().parent
options=subset.Options()
options.flavor='woff'
font=subset.load_font(str(ROOT/'assets/original/LXGWNeoXiHei.ttf'),options)
text=''.join((ROOT/f).read_text(encoding='utf-8') for f in ['app.py','index.html','app.js'])
processor=subset.Subsetter(options=options)
processor.populate(text=text)
processor.subset(font)
for record in font['name'].names:
    names={1:'CompanyText',2:'Regular',3:'CompanyText UI subset',4:'CompanyText',6:'CompanyText',16:'CompanyText',17:'Regular'}
    if record.nameID in names:
        record.string=names[record.nameID].encode(record.getEncoding(),errors='replace')
subset.save_font(font,str(ROOT/'assets/company.woff'),options)
