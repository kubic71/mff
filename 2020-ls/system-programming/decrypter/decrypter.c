#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


/* decrypt 64-bit block v with 128-bit key k */

#define DELTA 0x9e3779b9
#define SUM_INIT 0xC6EF3720
#define DECRYPT_KEY {128, 129, 130, 131}


static void decrypt(uint32_t* v, uint32_t* k) {
	uint32_t sum = SUM_INIT;

	for(int i = 0; i < 32; i++) {
		// substract from v[1]:

		v[1] -= ((v[0] << 4) + k[2]) ^
				(v[0]  + sum) ^
				((v[0] >> 5) + k[3]);

		v[0] -= ((v[1] << 4) + k[0]) ^
				(v[1]  + sum) ^
				((v[1] >> 5) + k[1]);

		sum -= DELTA;
	}
}


int main (int argc, char* argv[]) {

	if(argc != 3) {
		printf("Invalid number of paramenters\n");
		printf("Synopsis:\n");
		printf("$> decrypter input_file output_file\n");
		return 0;
	}

	char* input_filename = argv[1];
	char* output_filename = argv[2];

	// load the input file to memory
	FILE* f = fopen(input_filename, "r");

	uint32_t size;
	fread(&size, sizeof(uint32_t), 1, f);

	printf("File size: %d", size);

	// size padded to 8 bytes
	uint32_t size_padded = size % 8 == 0 ?  size  : (size / 8 + 1) * 8;
	
	uint32_t* data = malloc(size_padded);
	fread(data, 1, size_padded, f);

	/* decrypt chunks */ 
	uint32_t key[] = DECRYPT_KEY;

	uint32_t* chunk_ptr = data;
	for(uint32_t i = 0; i < size_padded / 8; i++) {
		decrypt(chunk_ptr, key);

		// go to the next 8B chunk
		chunk_ptr += 2;
	}

	fclose(f);

	/* save the decrypted content */
	FILE* out_f = fopen(output_filename, "w");
	fwrite(data, 1, size, out_f);
	fclose(out_f);

	// I don't have to explicitly call free, the execution ends here anyway
	
	return 0;
}



