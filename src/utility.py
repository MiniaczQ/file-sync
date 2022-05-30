def order_files(file1, file2):
    '''
    Orders files based on their last modification time.
    '''
    return (
        (file1, file2)
        if file1.stat().st_mtime < file2.stat().st_mtime
        else (file2, file1)
    )
