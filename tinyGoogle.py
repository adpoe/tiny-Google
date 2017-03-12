"""
    Main interface for the tinyGoogle client

    Functionality available:
    ------------------------
      a.  allow users to index documents
            ==> arg: -i filepath
      b.  enter search queries and retrieve relevant document objects
            ==> arg -s my keywords here
"""

import sys
import os
import subprocess

# define usage instructions to return when program is invoked incorrectly
usage = "\n\t>> tinyGoogle.py --> Usage Examples <<\n\t-----------------------------------------\n" \
        "\tIndex a new file:    " \
        "\tpython tinyGoogle.py -i /full/path/to/your/file/to/index.txt\n" \
        "\tSearch by keywords:  " \
        "\tpython tinyGoogle.py -s keywords to search\n\n"


def main():
    # ensure args are provided
    if len(sys.argv) < 2:
        print(usage)
        return

    """ INDEXING ACTION """
    if sys.argv[1] == '-i':
        # handle input errors
        if not len(sys.argv) == 3:
            print(usage + '\t\t * ERROR:  Please provide exactly one file to index, ensuring file path is valid.')
            return
        print('Indexing file: ' + sys.argv[2])
        # get current directory and use this info to call our files
        dir_path = os.path.dirname(os.path.realpath(__file__))
        shell_script = dir_path + '/index_file.sh'
        target_file = sys.argv[2]
        returncode = subprocess.call(['sh', shell_script, target_file])
        if not returncode == 0:
            print("\n\t\tTINY-GOOGLE :: --> INDEXING ERROR:   Please check filepath. File indexing failed. "
                  "\n\t\t\t\t\t\t     Full file path is needed. "
                  "\n\t\t\t\t\t\t     Try using the `pwd` command to get your current directory path.")


    """ SEARCHING ACTION """
    if sys.argv[1] == '-s':
        # handle input errors
        if len(sys.argv) < 3:
            print(usage + "\t\t * ERROR:  No keywords provided")
            return

        # build keywords list, we'll use this to search
        keywords = [sys.argv[k] for k in range(2, len(sys.argv))]
        print('Searching with keywords:  ' + str(keywords))

        # save keywords list to a file, so the query mapper/reducer can both
        # read same list of keywords, and inform their search effort
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fname = dir_path + '/search_keywords.txt'
        with open(fname, 'w') as f:
            f.write(str(keywords))

        # run the preprocessing shell script
        shell_script = dir_path + '/preprocess.sh'
        returncode = subprocess.call(['sh', shell_script])
        if not returncode == 0:
            print('\n\n\t\tTINY-GOOGLE:: ERROR --> __Preprocessing__ Failed')

        # run the inverted index shell script
        shell_script = dir_path + '/inverted_index_run.sh'
        returncode = subprocess.call(['sh', shell_script])
        if not returncode == 0:
            print('\n\n\t\tTINY-GOOGLE:: ERROR --> __Inverted Index__ MapReduce Job Failed')

        # run the query shell script
        shell_script = dir_path + '/query_run.sh'
        returncode = subprocess.call(['sh', shell_script])
        if not returncode == 0:
            print('\n\n\t\tTINY-GOOGLE:: ERROR --> __Query MapReduce__ Job Failed')


        """ CLEANUP """
        # Remove files from last run, so user can re-run the script
        shell_script = dir_path + '/cleanup.sh'
        returncode = subprocess.call(['sh', shell_script])
        if not returncode == 0:
            print('\n\n\t\tTINY-GOOGLE:: ERROR --> __CLEANUP__ Script Failed. You may need to delete Hadoop output directories manually.')

    return

if __name__ == "__main__":
    main()