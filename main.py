


def read(file):
	with open(file) as f:
		content = f.readlines();
		print content


def main():
	read('data/data0.txt')


if __name__ == "__main__":
    main()