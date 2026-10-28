import polib
import glob
import re
import os

def main():
    LANGUAGES = {
        'ar': 'Arabic',
        'bn': 'Bangla',
        'de': 'German',
        'es': 'Spanish',
        'fa': 'Persian',
        'fr': 'French',
        'he': 'Hebrew',
        'hy_am': 'Armenian',
        'hi_in': 'Hindi',
        'id': 'Indonesian',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'pl': 'Polish',
        'pt-br': 'Portuguese, Brazil',
        'pt-pt': 'Portuguese',
        'ru': 'Russian',
        'sq': 'Albanian',
        'sv': 'Swedish',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'vi': 'Vietnamese',
        'zh-tw': 'Chinese, Taiwan',
        'zh': 'Chinese'
    }

    readme_path = 'README.md'
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()

    table_lines = ['| Language | % |', '| --- | --- |']
    total_strings = 0
    total_translated = 0

    files = sorted(glob.glob('dicts/dict_*.po'))
    
    for file in files:
        lang_code = os.path.basename(file).replace('dict_', '').replace('.po', '')
        
        if lang_code.lower() == 'en':
            continue
            
        po = polib.pofile(file)
        
        lang_name = LANGUAGES.get(lang_code.lower(), lang_code)
        
        valid_entries = [e for e in po if not e.obsolete]
        
        t_total = len(valid_entries)
        t_trans = len([e for e in valid_entries if e.translated()])
        
        total_strings += t_total
        total_translated += t_trans
        
        percent = int((t_trans / t_total) * 100) if t_total > 0 else 0
        color = 'brightgreen' if percent >= 90 else 'yellow' if percent >= 50 else 'red'
        
        badge_url = f'https://img.shields.io/badge/progress-{percent}%25-{color}'
        file_url = f'https://github.com/horsicq/XTranslation/blob/master/dicts/dict_{lang_code}.po'
        
        row = f'| {lang_name:<20} | <a href="{file_url}"> <img src="{badge_url}" /> </a> |'
        table_lines.append(row)

    overall_percent = int((total_translated / total_strings) * 100) if total_strings > 0 else 0
    overall_color = 'brightgreen' if overall_percent >= 90 else 'yellow' if overall_percent >= 50 else 'red'
    main_badge = f'![Overall](https://img.shields.io/badge/Translation_Progress-{overall_percent}%25-{overall_color})'

    table_text = '\n'.join(table_lines)
    
    readme = re.sub(
        r'<!-- PO_TABLE_START -->.*<!-- PO_TABLE_END -->', 
        f'<!-- PO_TABLE_START -->\n{table_text}\n<!-- PO_TABLE_END -->', 
        readme, 
        flags=re.DOTALL
    )
    
    readme = re.sub(
        r'<!-- PO_BADGE_MAIN_START -->.*<!-- PO_BADGE_MAIN_END -->', 
        f'<!-- PO_BADGE_MAIN_START -->\n{main_badge}\n<!-- PO_BADGE_MAIN_END -->', 
        readme, 
        flags=re.DOTALL
    )

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)

if __name__ == "__main__":
    main()