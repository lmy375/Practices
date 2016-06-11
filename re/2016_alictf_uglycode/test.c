#include <stdio.h>

char sub_603380(int a1)
{
  int v2; // [sp+14h] [bp-8h]@1
  char v3; // [sp+19h] [bp-3h]@1
  int i; // [sp+1Ah] [bp-2h]@1

  v3 = 0;
  v2 = 0;
  for ( i = 1; i < a1 + 1; ++i )
  {
    if ( i & 1 )
    {
      if ( i == 3 * (((unsigned int)(0x5556 * i) >> 16) - (i >> 15)) )
        ++v2;
    }
    else
    {
      ++v2;
    }

    if ( v2 == 19509 ){// add this
      printf("%#x", i);
      break;
    }
  }
  if ( v2 == 19509 )
    v3 = 1;
  return v3;
}

char sub_603440(unsigned int a1)
{
  int v2; // [sp+1Ch] [bp-10h]@1
  char v3; // [sp+27h] [bp-5h]@1
  unsigned int i; // [sp+28h] [bp-4h]@1

  v3 = 0;
  v2 = 0LL;
  //for ( i = 1; a1 + 1 > i; ++i )
  for ( i = 1; a1 + 1 < i; ++i )
  {
    if ( i & 1 )
    {
      if ( i % 3 )
      {
        if ( i % 5 )
        {
          if ( !(i % 7) )
            ++v2;
        }
        else
        {
          ++v2;
        }
      }
      else
      {
        ++v2;
      }
    }
    else
    {
      ++v2;
    }

    if ( v2 == 665543088 ){// add this
      printf("%#x\n",i );
      break;
    }
  }
  if ( v2 == 665543088 )
    v3 = 1;
  return v3;
}

int main(int argc, char const *argv[])
{
  int i = 0;
  sub_603380(0xFFFF);
  sub_603440(0xFFFFFFFF);
  
  return 0;
}