#include <stdio.h>

static int const LINES = 20000;

int * read(FILE *file, int *ddf, int size)
{
	int i = 0;
	int value;

	for (int i = 0; i < size; ++i)
	{
		// Skip first LINE!
		if (i != 0)
		{
			fscanf(file, "%d", &value);
			ddf[i] = value;
		}
		else
		{
			fscanf(file, "%*[^\n]\n", NULL);
		}
	}

	fclose(file);

	return ddf;
}

int main()
{
	FILE *file = fopen("data/data0.txt", "r");   

	int ddf[LINES];
	read(file, ddf, LINES);

	for (int i = 0; i < 200; ++i)
	{
		printf("%d\n", ddf[i]);
	}

	return 0;
}