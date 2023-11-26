class BookReference:
    """Class that describes a reference of type Book

        Mandatory arguments:
            -ref_key, author, title, year, publisher
        Optional arguments:
            -editor, volume, pages
    """
    def __init__(self, ref_key, author, title, year, publisher):
        self.ref_key = ref_key
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher
        # self.editor = editor
        # self.volume = volume
        # self.pages = pages

    def __str__(self):
        return (
            f"{self.ref_key:<10} {self.author:<25} {self.title:<35} {self.year:<10} {self.publisher:<15}"
        )
