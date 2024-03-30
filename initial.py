"""
This module contains tools for reading data useful data from files.
"""

# ------------------------------------------------------------------------------
# imports

# ------------------------------------------------------------------------------

def get_authors(file_path: str) -> list:
    """
    Extracts the authors from a .bib file.

    Parameters
    ----------
    file_path : str
        The path to the .bib file.

    Returns
    -------
    list
        A list of authors formatted as 'Firstname Lastname'.
    """
    authors = []
    with open(file_path) as f:
        for line in f:
            if 'author = ' in line:
                names_only = line.split('{')[1].split('}')[0]
                split_names = names_only.split(' and ')
                authors = []
                for name in split_names:
                    last, first = name.split(', ')
                    authors.append(f'{first} {last}')
    return authors

# ------------------------------------------------------------------------------

def get_title(file_path: str) -> str:
    """
    Extracts the title from a .bib file.

    Parameters
    ----------
    file_path : str
        The path to the .bib file.

    Returns
    -------
    str
        The title of the paper.
    """
    with open(file_path) as f:
        for line in f:
            if 'title = ' in line:
                title_arg = line.split('= ')[1].split(',\n')[0]
                title = title_arg.replace('{', '').replace('}', '')
                return title

# ------------------------------------------------------------------------------
            
def get_filename(file_path: str) -> str:
    """
    Extracts the title from a .bib file and formats it as a markdown filename.

    Parameters
    ----------
    file_path : str
        The path to the .bib file.

    Returns
    -------
    str
        The title of the paper formatted as a filename.
    """
    title = get_title(file_path)
    savename = ''.join(char for char in title if char.isalnum())
    savefile = f'{savename}.md'
    return savefile

# ------------------------------------------------------------------------------

def create_markdown(
        save_dir: str,
        file_name: str,
        title: str,
        authors: list
    ) -> None:
    """
    Creates a markdown file with the given information.

    Parameters
    ----------
    save_dir : str
        The directory to save the markdown file.
    file_name : str
        The name of the markdown file.
    title : str
        The title of the paper.
    authors : list
        A list of authors formatted as 'Firstname Lastname'.
    
    Returns
    -------
    None
    """
    with open(save_dir + file_name, 'w') as f:
        f.write(f'# {title}\n\n')
        f.write('## Authors\n\n')
        for author in authors:
            f.write(f'- [[{author}]]\n')

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    filepath = 'local/single.bib'
    savedir = 'local/'
    
    authors = get_authors(filepath)
    title = get_title(filepath)
    filename = get_filename(filepath)

    create_markdown(savedir, filename, title, authors)