#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define _VERSION "1.12"

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
 
    *output_length = 4 * ((input_length + 2) / 3); // added +1 for \0
 
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

int sendMessage(char * message_content, int message_length) {
	
	if (message_length == 0) message_length = strlen(message_content);
	
	fwrite(&message_length,sizeof(int),1,stdout);
	printf("%s", message_content);
	fflush(stdout);
}

char * readBinaryFileToBase64(char * path, FILE * fp) {
	
	FILE *ifp;
	long size = 0;

	if ((ifp = fopen(path, "rb")) == NULL) {
		fprintf(fp, "%s\tError reading file\n", getTime());
		fprintf(stderr, "%s\tError reading file\n", getTime());
		fclose(fp);
		sendMessage("{\"error\": \"Error reading file\"}", 0);
		exit(1);
	}
	
	fseek(ifp, 0L, SEEK_END);
	size = ftell(ifp);
	rewind(ifp);
	
	char new_array[size];
	fread( new_array, sizeof(char), size, ifp);
	fclose(ifp);

	size_t base64_len;
	char * base64_str = base64_encode((char*)new_array, size, &base64_len);	

	base64_str = realloc(base64_str,base64_len + 1);
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
	#ifdef _WIN32 
		_setmode(_fileno(stdin), _O_BINARY);
		_setmode(_fileno(stdout), _O_BINARY);
	#else
		freopen(NULL, "rb", stdin);
		freopen(NULL, "wb", stdout);
	#endif

	if( argc == 2 ) {
		
		if(strcmp(argv[1],"--debug")==0) {

			exit(0);
		}
		
	}

	FILE * fp;
	
	if ((fp = fopen("error.log", "a")) == NULL) {
		fprintf(stderr, "Can't open error.log\n");
		sendMessage("{\"error\": \"Cannot open log file\"}", 0);
		return 0;
	}
		
	int size;
	fread(&size, sizeof(int), 1, stdin);

	char buf[size];
	fread(&buf, sizeof(char), size, stdin);
	
	fflush(stdin);

	char sub[size];
	substring(buf, sub, 15, size - 18);
	
	if(strstr(buf, "%version%") != NULL) {
		char message_content[128];
		sprintf(message_content,"{\"version\": \"%s\"}",_VERSION);
		fclose(fp);
		sendMessage(message_content,0);
		return 0;
	}
		
	struct stat buffer;
	char mod_time[64];
 
	if( stat( sub, &buffer ) != 0 ) {
		fprintf(fp, "%s\tError reading file\n", getTime());
		fprintf(stderr, "%s\tError reading file\n", getTime());
		fclose(fp);
		sendMessage("{\"error\": \"Error reading file\"}", 0);
		exit(1);
	} else {
		sprintf( mod_time, "%s", ctime(&buffer.st_mtime)  );
		mod_time[strlen(mod_time) - 1] = '\0';
	}
		
	char * blah = (char*) buf;
	if(strstr(blah, "!@!@") != NULL) {
		char message_content[128];
		sprintf(message_content,"{\"last_mod\": \"%s\"}",&mod_time);
		fclose(fp);
		sendMessage(message_content,0);
		return 0;
	}

	char * base64data = readBinaryFileToBase64(sub, fp);
	
	if (base64data == NULL) {
		fprintf(stderr, "%s\tError encoding file\n", getTime());
		fclose(fp);
		sendMessage("{\"error\": \"Base64 encoding was unsuccessful\"}",0);
		exit(1);
	}

	char message_content[strlen(base64data) + 128];
	
	int message_len = sprintf(	message_content,
								"{\"last_mod\": \"%s\", \"base64\": \"%s\"}",
								&mod_time,
								base64data
	);
	
	free(base64data);

	fclose(fp);
	sendMessage(message_content, 0);

    return 0;
}

