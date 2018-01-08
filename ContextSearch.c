#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

static char encoding_table[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
                                'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                'w', 'x', 'y', 'z', '0', '1', '2', '3',
                                '4', '5', '6', '7', '8', '9', '+', '/'};
								
static int mod_table[] = {0, 2, 1};

char *base64_encode(const unsigned char *data,
                    size_t input_length,
                    size_t *output_length) {
 
    *output_length = 4 * ((input_length + 2) / 3);
 
    char *encoded_data = malloc(*output_length);
    if (encoded_data == NULL) return NULL;
	int i, j;
    for ( i = 0, j = 0; i < input_length;) {
 
        uint32_t octet_a = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_b = i < input_length ? (unsigned char)data[i++] : 0;
        uint32_t octet_c = i < input_length ? (unsigned char)data[i++] : 0;
 
        uint32_t triple = (octet_a << 0x10) + (octet_b << 0x08) + octet_c;
 
        encoded_data[j++] = encoding_table[(triple >> 3 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 2 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 1 * 6) & 0x3F];
        encoded_data[j++] = encoding_table[(triple >> 0 * 6) & 0x3F];
    }
 
    for ( i = 0; i < mod_table[input_length % 3]; i++)
        encoded_data[*output_length - 1 - i] = '=';
 
    return encoded_data;
}

char * getTime() {
	time_t t = time(NULL);
	char * str = ctime(&t);
	str[strlen(str) -1] = '\0';
	return str;
}

char * readBinaryFileToBase64(char * path, FILE * fp) {
	
	FILE *intArrayFile;
	long size = 0;

	intArrayFile = fopen(path, "rb");
	
	if (intArrayFile == NULL) {
		fprintf(fp, "%s\tCan't open %s\n", getTime(), path);
		fclose(fp);
		exit(1);
	}
	
	fseek(intArrayFile, 0L, SEEK_END);
	size = ftell(intArrayFile);
	rewind(intArrayFile);
	
	char new_array[size];
	fread( new_array, sizeof(char), size, intArrayFile);

	size_t base64_len;
	char * base64_str = base64_encode((char*)new_array, size, &base64_len);	
	base64_str[base64_len] = '\0';

	return base64_str;
}

void substring(char s[], char sub[], int p, int l) {
   int c = 0;
 
   while (c < l) {
      sub[c] = s[p+c-1];
      c++;
   }
   sub[c] = '\0';
}

int main(int argc, char *argv[])
{	
	if( argc == 2 ) {
		
		if(strcmp(argv[1],"--debug")==0) {

		}
		
		exit(0);
	}

	FILE * fp;
	
	if ((fp = fopen("error.log", "a")) == NULL) {
		perror("Can't open error.log\n");
		exit(1);
	}
	
	freopen(NULL, "rb", stdin);
	freopen(NULL, "wb", stdout);
	
	#ifdef _WIN32 
    	_setmode(_fileno(stdin), _O_BINARY);
		_setmode(_fileno(stdout), _O_BINARY);
	#endif	

	
	int size;
	fread(&size, sizeof(int), 1, stdin);

	char buf[size];
	fread(&buf, size, 1, stdin);

	fprintf(fp, "%s\tReceived %d bytes\n",getTime(),size);

	char sub[size];
	substring(buf, sub, 15, size - 18);
	
	struct stat buffer;
	char mod_time[64];
 
	if( stat( sub, &buffer ) != 0 ) {
		fprintf(fp, "%s\tError reading file\n", getTime());
		perror("Error reading file\n");
		exit(1);
	} else {
		sprintf( mod_time, "%s", ctime(&buffer.st_mtime)  );
		mod_time[strlen(mod_time) - 1] = '\0';
	}
	
	char * base64data;
	if(strstr(buf, "!@!@") != NULL) {
		fprintf(fp, "%s\tRequest for time only\n", getTime());
		base64data = "";
	} else {	
		base64data = readBinaryFileToBase64(sub, fp);
	}	

	char message_content[strlen(base64data) + 128];
	
	int message_len = sprintf(	message_content,
								"{\"last_mod\": \"%s\", \"base64\": \"%s\"}",
								&mod_time,
								base64data
	);

	fwrite(&message_len,sizeof(int),1,stdout);
	printf("%s", message_content);

	fprintf(fp, "%s\tSent %d bytes\n", getTime(), message_len);
	fclose(fp);

    return 0;
	
	// good	35593
	// bad	35594
	// bad	69046
	// bad	68350
}

