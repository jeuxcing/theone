
#ifndef CONFIG_H
#define CONFIG_H


struct config_s
{
	char* ssid;
	char* password;
	char* server_ip;
	int server_port;
};
typedef struct config_s config_t;

const size_t num_configs = 1;

const config_t configs[num_configs] = {
	{
		"BimYo",
		"Le voila le mot de passe !",
		"192.168.1.71",
		4040
	}
};

#endif