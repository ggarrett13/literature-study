
# for file, directory in chapters
#   if file.endswith('.tex'): then execute pandoc on file
import os
import re 
import subprocess
import sys

REGEX_SUBSTITUTION = {
    r'\\glsposs{(\w+)}': r"\1's",
}

def preprocess(directory):
    # make a copy of the directory and place into temporary directory.
    # then iterate over the temporary directory recursively, subtituting and overwriting
    # the contents of each file.

    # get abspath of temporary directory
    temp_path = os.path.abspath(os.path.join(root, 'temp'))
    # create temporary directory, if exists, allow overwrite
    os.makedirs(temp_path, exist_ok=True)
    # iterate over directory recursively, substituting and overwriting
    # the contents of each file
    for file in os.listdir(directory):
        # if file is a .tex file, execute pandoc on it
        if file.endswith('.tex'):
            # get abspath of file
            file_path = os.path.abspath(os.path.join(directory, file))
            # get abspath of temporary directory
            temp_file_path = os.path.abspath(os.path.join(temp_path, file))
            # copy file to temporary directory
            os.system('cp ' + file_path + ' ' + temp_file_path)
            # open file in temporary directory
            with open(temp_file_path, 'r') as f:

                # read file contents
                contents = f.read()

                # contents = re.escape(contents)
                for key, value in REGEX_SUBSTITUTION.items():
                        contents = re.sub(key, value, contents, flags=re.MULTILINE)

                with open(temp_file_path, 'w') as f:
                    f.write(contents)
        # if file is a directory, recurse on it
        elif os.path.isdir(os.path.join(directory, file)):
            preprocess(os.path.join(directory, file))
        # otherwise, ignore file
        else:
            pass


def pandoc(directory):
    # get all .tex files in directory, and execute pandoc on each,
    # creating an .md file with the same name as the .tex file, and 
    # placing it in the same directory structure, relative to "output" directory
    for file in os.listdir(directory):

        # if file is a .tex file, execute pandoc on it
        if file.endswith('.tex'):
            # get abspath of file
            file_path = os.path.abspath(os.path.join(directory, file))
            # get abspath of output directory
            output_path = os.path.abspath(os.path.join(root, 'out'))
            # get abspath of output file
            output_file_path = os.path.abspath(os.path.join(output_path, file.replace('.tex', '.md')))
            # execute pandoc on file
            subprocess.call(['pandoc',  file_path,'-o', output_file_path,  '--bibliography', os.path.join(root, 'library.bib'), '--csl', os.path.join(root, 'styles/elsevier-with-titles'),
            '-t', 'gfm', '--citeproc', 
            '--wrap', 'none',
            '--metadata', 'link-citations=true', 
            # '--metadata', 'suppress-bibliography=false',
            # '--metadata', 'reference-section-title=References'
            ])
            # print output file path
            print(output_file_path)
            # print newline
            print()
        # if file is a directory, recurse on it
        elif os.path.isdir(os.path.join(directory, file)):
            function(os.path.join(directory, file))
        # otherwise, ignore file
        else:
            pass



if __name__ == "__main__":


    if len(sys.argv) < 2:
        print("Usage: pandoc.py <directory>")
        sys.exit(1)

    # get abspath of directory
    directory = os.path.abspath(sys.argv[1])

    # set root as path of script + "/output"
    root = os.path.dirname(os.path.abspath(__file__))

    # if directory does not exist, create it
    if not os.path.exists(root):
        os.makedirs(root)


    preprocess(directory)
    pandoc("temp")
    # remove temporary directory
    os.system('rm -rf temp')

    print("Done")
    sys.exit(0)