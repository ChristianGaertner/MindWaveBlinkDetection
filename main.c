#include <stdio.h>

static int const LINES = 20000;
static int const MAX_CLUSTERS = 50;
static int const PEAK_DET_THRESHOLD = 500;

int * read(FILE *file, int *ddf)
{
	int i = 0;
	int value;

	for (int i = 0; i < LINES; ++i)
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

int * peakdet(int *data, int threshold, int *indices)
{
	int indicesCounter = 0;
	for (int i = 0; i < LINES; ++i)
	{
		if (data[i] > threshold)
		{
			indices[indicesCounter] = i;
			indicesCounter++;
		}
	}

	return indices;
}

int main()
{
	FILE *file = fopen("data/data0.txt", "r");   

	int ddf[LINES];
	int indices[LINES];

	read(file, ddf);
	peakdet(ddf, PEAK_DET_THRESHOLD, indices);

	for (int i = 0; i < LINES; ++i)
	{
		printf("%d\n", indices[i]);
	}

	return 0;
}