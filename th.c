#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "MT.h"

#define TRUE 1
#define FALSE 0

int yaochu[13] = {0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33};


char * node_create() {
	char * p;
	if ((p = (char *) malloc(sizeof(char) * 9)) == NULL)
	{
		printf("error\n");
		exit(0);
	}

	int i;
	for (i = 0; i < 9; i++)
	{
		p[i] = 0;
	}

	return p;
}


void node_print(char * p)
{
	int i;
	for (i = 0; i < 9; i++)
	{
		printf("%d ", p[i]);
	}
	printf("\n");
}


int node_is_empty(char * p)
{
	int flg = TRUE;
	int i;
	for (i = 0; i < 9; i++)
	{
		if (p[i] != 0)
		{
			flg = FALSE;
			break;
		}
	}
	return flg;
}


char * node_copy(char * p)
{
	char * q = node_create();
	int i;
	for (i = 0; i < 9; i++)
	{
		q[i] = p[i];
	}
	return q;
}


char * reduce_head(char * p, int index)
{
	char * q;
	if (p[index] >= 2)
	{
		q = node_copy(p);
		q[index] -= 2;
	}
	else
	{
		q = NULL;
	}
	return q;
}


char * reduce_tri(char * p, int index)
{
	char * q;
	if (p[index] >= 3)
	{
		q = node_copy(p);
		q[index] -= 3;
	}
	else
	{
		q = NULL;
	}
	return q;
}

char * reduce_seq(char * p, int index)
{
	char * q;
	if (p[index] >= 1 &&
		p[(index + 1)] >= 1 &&
		p[(index + 2)] >= 1)
	{
		q = node_copy(p);
		q[index] -= 1;
		q[(index + 1)] -= 1;
		q[(index + 2)] -= 1;
	}
	else
	{
		q = NULL;
	}
	return q;
}


int reduce_seq_rec(char * p, int index)
{
	if (index > 8)
	{
		return node_is_empty(p);
	}

	char * q;
	q = reduce_seq(p, index);
	if (q == NULL)
	{
		return reduce_seq_rec(p, (index + 1));
	}
	else
	{
		return reduce_seq_rec(q, index);
	}
}


int reduce_tri_rec(char * p, int index)
{
	if (index > 8)
	{
		return reduce_seq_rec(p, 0);
	}
	else
	{
		char * q;
		q = reduce_tri(p, index);
		if (q == NULL)
		{
			return reduce_tri_rec(p, (index + 1));
		}
		else
		{
			return reduce_tri_rec(q, (index + 1)) || reduce_tri_rec(p, (index + 1));
		}
	}
}


int is_complete_jihai(char * p)
{
	int cnt_head = 0;
	int i;
	for (i = 0; i < 7; i++)
	{
		if (p[i] == 2)
		{
			cnt_head++;
			if (cnt_head >= 2)
			{
				return FALSE;
			}
		}
		else if (p[i] != 0 && p[i] != 3)
		{
			return FALSE;
		}
	}
	return TRUE;
}


int is_complete_suit(char * p)
{
	// 頭を取らない場合
	if (reduce_tri_rec(p, 0))
	{
		return TRUE;
	}

	//頭を取る場合(取れるものに関しては)
	int i;
	for (i = 0; i < 9; i++)
	{
		char * q;
		q = reduce_head(p, i);
		if (q != NULL)
		{
			if (reduce_tri_rec(q, 0))
			{
				return TRUE;
			}
		}
	}
	return FALSE;
}


int seven_pairs_complete(char * p)
{
	int cnt_pairs = 0;
	int i;
	for (i = 0; i < 34; i++)
	{
		if (p[i] == 2)
		{
			cnt_pairs++;
		}
		else if (p[i] != 0)
		{
			return FALSE;
		}
	}
	return (cnt_pairs == 7);
}


int thirteen_orphants_complete(char * p)
{
	int cnt_pairs = 0;
	int i;
	for (i = 0; i < 13; i++)
	{
		if (p[yaochu[i]] == 2)
		{
			if (cnt_pairs == 1)
			{
				return FALSE;
			}
			else
			{
				cnt_pairs++;
			}
		}
		else if (p[yaochu[i]] != 1)
		{
			return FALSE;
		}
	}
	return TRUE;
}


int count_tiles(char *p, int len)
{
	int sum = 0;
	int i;
	for (i = 0; i < len; i++)
	{
		sum += p[i];
	}
	return sum;
}


int is_complete(char * p)
{
	// 各色の枚数チェック
	int cnt_head = 0;
	int mod_m, mod_p, mod_s, mod_j;
	
	mod_m = count_tiles(p, 9) % 3;
	mod_p = count_tiles((p + 9), 9) % 3;
	mod_s = count_tiles((p + 18), 9) % 3;
	mod_j = count_tiles((p + 27), 7) % 3;

	// 半端な1枚が出るときはfalse
	if ((mod_m == 1) || (mod_p == 1) || (mod_s == 1) || (mod_j == 1))
	{
		return FALSE;
	}

	// 頭が2つ以上のときはfalse
	if ((((mod_m == 2) ? 1 : 0) + ((mod_p == 2) ? 1 : 0) + ((mod_s == 2) ? 1 : 0) + ((mod_j == 2) ? 1 : 0)) >= 2)
	{
		return FALSE;
	}

	// 牌理的に揃ってるか
	return is_complete_suit(p) && is_complete_suit(p + 9) && is_complete_suit(p + 18) && is_complete_jihai(p + 27);
}


// 配牌作成
char * get_random_spec()
{
	// 牌を生成
	char tiles[136];
	char * p = tiles;
	int i;
	for (i = 0; i < 34; i++)
	{
		*p = (char)i;p++;
		*p = (char)i;p++;
		*p = (char)i;p++;
		*p = (char)i;p++;
	}

	// ランダムに並び替え
	char tmp;
	int num;
	for (i = 0; i < 136; i++)
	{
		num = genrand_int32() % 136;
		tmp = tiles[i];
		tiles[i] = tiles[num];
		tiles[num] = tmp;
	}

	// 牌の種類ごとに度数をカウント
	char * spec;
	if ((spec = (char *)malloc(sizeof(char) * 34)) == NULL)
	{
		printf("Error.\n");
		exit(0);
	}
	for (i = 0; i < 34; i++)
	{
		spec[i] = 0;
	}
	for (i = 0; i < 14; i++)
	{
		spec[(int)tiles[i]]++;
	}

	return spec;
}


void spec_print(char * spec)
{
	int i;
	int j;
	for (i = 0; i < 9; i++)
	{
		for (j = 0; j < spec[i]; j++)
		{
			printf("%d", (i + 1));
		}
	}
	printf(",");

	for (i = 9; i < 18; i++)
	{
		for (j = 0; j < spec[i]; j++)
		{
			printf("%d", (i - 8));
		}
	}
	printf(",");

	for (i = 18; i < 27; i++)
	{
		for (j = 0; j < spec[i]; j++)
		{
			printf("%d", (i - 17));
		}
	}
	printf(",");

	for (i = 27; i < 34; i++)
	{
		for (j = 0; j < spec[i]; j++)
		{
			printf("%d", (i - 26));
		}
	}
	printf(",");
	// printf("\n");
}


int main (int argc, char *argv[])
{
	// 乱数の初期化
	init_genrand((unsigned)time(NULL));

	int cnt = 0;

	char * p;
	while (TRUE)
	{
		cnt++;
		p = get_random_spec();
		if (seven_pairs_complete(p))
		{
			spec_print(p);
			printf("seven_pairs,%d\n", cnt);
			break;
		}
		else if (thirteen_orphants_complete(p))
		{
			spec_print(p);
			printf("thirteen_orphants,%d\n", cnt);
			break;
		}
		else if (is_complete(p))
		{
			spec_print(p);
			printf("normal,%d\n", cnt);
			break;
		}
	}

	return 0;
}
