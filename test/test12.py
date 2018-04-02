class A:
    def __enter__(self):
        print(1234)

    def __exit__(self):
        print('sdfafa')


with A():
    pass