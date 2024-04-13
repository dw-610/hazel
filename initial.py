"""
This module contains tools for reading data useful data from files.
"""

# ------------------------------------------------------------------------------
# imports

import os
import re
from typing import TextIO

# ------------------------------------------------------------------------------

def get_authors(file: TextIO) -> list:
    """
    Extracts the authors from a .bib file.

    Parameters
    ----------
    file : TextIO
        The file object of the .bib file.

    Returns
    -------
    list
        A list of authors formatted as 'Firstname Lastname'.
    """
    authors = []
    for line in file:
        if 'author = ' in line:
            names_only = line.split('{')[1].split('}')[0]
            split_names = names_only.split(' and ')
            authors = []
            for name in split_names:
                clean_name = re.sub(r'[^\w\s ,]', '', name, flags=re.UNICODE)
                last, first = clean_name.split(', ')
                authors.append(f'{first} {last}')
    file.seek(0) # reset the pointer
    return authors

# ------------------------------------------------------------------------------

def get_title(file: TextIO) -> str:
    """
    Extracts the title from a .bib file.

    Parameters
    ----------
    file : TextIO
        The file object of the .bib file.
    
    Returns
    -------
    str
        The title of the paper.
    """
    for line in file:
        if 'title = ' in line:
            title_arg = line.split('= ')[1].split(',\n')[0]
            title = title_arg.replace('{', '').replace('}', '')
            file.seek(0) # reset the pointer
            return title

# ------------------------------------------------------------------------------
        
def get_year(file: TextIO) -> str:
    """
    Extracts the year from a .bib file.

    Parameters
    ----------
    file : TextIO
        The file object of the .bib file.
    
    Returns
    -------
    str
        The year the paper was published.
    """
    for line in file:
        if 'year = ' in line:
            year = line.split('{')[1].split('}')[0]
            file.seek(0) # reset the pointer
            return year

# ------------------------------------------------------------------------------
            
def get_filename(title: str) -> str:
    """
    Extracts the title from a .bib file and formats it as a markdown filename.

    Parameters
    ----------
    title : str
        The title of the paper, returned from the get_title function.

    Returns
    -------
    str
        The title of the paper formatted as a filename.
    """
    savename = ''.join(char for char in title if char.isalnum())
    savefile = f'{savename}.md'
    return savefile

# ------------------------------------------------------------------------------

def get_tags(file: TextIO) -> list:
    """
    Extracts the tags that were set in Zotero from a .bib file.

    Parameters
    ----------
    file : TextIO
        The file object of the .bib file.
    
    Returns
    -------
    tuple of lists
        A tuple containing two lists: the first list contains the status tags
        and the second list contains the topic tags.
    """
    status_tags = []
    topic_tags = []
    for line in file:
        if 'keywords = ' in line:
            tag_str = line.split('{')[1].split('}')[0]
            split_tags = tag_str.split(', ')
            for tag in split_tags:
                if tag == 'To Read - Low Priority':
                    status_tags.append('low-priority')
                elif tag == 'To Read - Mid Priority':
                    status_tags.append('mid-priority')
                elif tag == 'To Read - High Priority':
                    status_tags.append('high-priority')
                elif tag == '1st Pass':
                    status_tags.append('first-pass')
                elif tag == '2nd Pass':
                    status_tags.append('second-pass')
                elif tag == '3rd Pass':
                    status_tags.append('third-pass')
                elif tag == 'Important':
                    status_tags.append('important')
                elif tag == 'Archived':
                    pass
                else:
                    # convert the tag to kebab case
                    tag = '-'.join(tag.lower().split(' '))
                    topic_tags.append(tag)
    if len(status_tags) == 0:
        status_tags.append('not-read')
    file.seek(0) # reset the pointer
    return status_tags, topic_tags

# ------------------------------------------------------------------------------
        
def get_notes(file: TextIO) -> str:
    """
    Extracts the notes from a .bib file.

    Parameters
    ----------
    file : TextIO
        The file object of the .bib file.
    
    Returns
    -------
    list
        A list of notes from the .bib file.
    """
    flag = False
    notes = []
    for line in file:
        if 'annote = ' in line:
            flag = True
            continue
        if flag:
            if '},' in line:
                flag = False
                break
            else:
                notes.append(line.strip())
    file.seek(0) # reset the pointer
    return notes

# ------------------------------------------------------------------------------

def get_url(file: TextIO) -> str:
    """
    Extracts the URL from a .bib file.

    Parameters
    ----------
    file : TextIO
        The file object of the .bib file.
    
    Returns
    -------
    str
        The URL of the paper.
    """
    for line in file:
        if 'url = ' in line:
            url = line.split('{')[1].split('}')[0]
            file.seek(0) # reset the pointer
            return url
    return None

# ------------------------------------------------------------------------------

def extract_data(file_path: str) -> dict:
    """
    Extracts information from a .bib file.

    Parameters
    ----------
    file_path : str
        The path to the .bib file.

    Returns
    -------
    dict
        A dictionary containing the data extracted from the .bib file.
    """
    with open(file_path) as file:
        title = get_title(file)
        authors = get_authors(file)
        filename = get_filename(title)
        status_tags, topic_tags = get_tags(file)
        imported_notes = get_notes(file)
        url = get_url(file)
        year = get_year(file)
        return {
            'title': title,
            'authors': authors,
            'filename': filename,
            'status_tags': status_tags,
            'topic_tags': topic_tags,
            'imported_notes': imported_notes,
            'url': url,
            'year': year
        }

# ------------------------------------------------------------------------------

def create_markdown(save_dir: str, data_dictionary: dict) -> None:
    """
    Creates a markdown file with the given information.

    Parameters
    ----------
    save_dir : str
        The directory where the markdown file will be saved.
    data_dictionary : dict
        A dictionary containing the data extracted from the .bib file.
        This is the output of the extract_data function.
    
    Returns
    -------
    None
    """
    title = data_dictionary['title']
    authors = data_dictionary['authors']
    file_name = data_dictionary['filename']
    status_tags = data_dictionary['status_tags']
    topic_tags = data_dictionary['topic_tags']
    imported_notes = data_dictionary['imported_notes']
    url = data_dictionary['url']
    year = data_dictionary['year']

    with open(save_dir + file_name, 'w') as f:
        f.write(f'# {title} ({year})\n\n')

        if url is not None:
            f.write(f'[Link to Online Version]({url})\n\n')
        else:
            f.write('(Link not found)\n\n')

        f.write('## Tags\n\n')
        for tag in status_tags:
            f.write(f'#{tag}\n')
        if len(status_tags) > 0: 
            f.write('\n')
        for tag in topic_tags:
            f.write(f'#{tag}\n')
        if len(topic_tags) > 0: 
            f.write('\n')

        f.write('## Authors\n\n')
        for author in authors:
            names = author.split(' ')
            scored = '_'.join(names)
            f.write(f'- [[PPL_{scored}|{author}]]\n')
        f.write('\n')

        f.write('## Summary\n\n')
        f.write('(Summary here)\n\n')
        f.write('## Key Takeaways\n\n')
        f.write('- Key takeaways here\n\n')
        f.write('## Relevance (or lack thereof)\n\n')
        f.write('(Relevance here)\n\n')

        if len(imported_notes) > 0:
            f.write('## Imported Notes\n\n')
            for note in imported_notes:
                f.write(f'- {note}\n')
            f.write('\n')
        f.write('---------------\n')  
        f.write('*Made with Hazel*\n')

# ------------------------------------------------------------------------------
        
def split_bibs(file_path: str) -> None:
    """
    Splits a .bib file with multiple entries into individual .bib files.

    Parameters
    ----------
    file_path : str
        The path to the .bib file to be split.
    
    Returns
    -------
    None
    """
    with open(file_path) as file:
        bibs = file.read().split('@')
        for i, bib in enumerate(bibs):
            if i == 0:
                continue
            with open(f'bibs/{i}.bib', 'w') as f:
                f.write(f'@{bib}')

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    
    bib = 'local/gardenfors.bib'
    savedir = 'local/'   

    data = extract_data(bib)

    create_markdown(savedir, data) 

    # for file in os.listdir('bibs'):
    #     filepath = f'bibs/{file}'
    #     data = extract_data(filepath)
    #     create_markdown(savedir, data)

    # for key, value in data.items():
    #     print(f'{key}: {value}')

    # create_markdown(savedir, data)

    # filepath = 'local/sem-comm.bib'
    # split_bibs(filepath)