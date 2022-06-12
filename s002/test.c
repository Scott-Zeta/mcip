#include <unistd.h>

void putnbr(int num)
{
    char c;
    while(num > 9)
    {
        c = (num % 10) + '0';
        write(1, &c, 1);
        num = num / 10;
    }
    c = num + '0';
    write (1, &c, 1);
}

int main(void)
{
    int i;

    i = 0;
    while (i <= 100)
    {
        if (i % 3 == 0 && i % 5 == 0)
        {
            write(1, "fizzbuzz\n", 9);
        }
        else if(i % 3 == 0)
        {
            write(1, "fizz\n", 5);
        }
        else if(i % 5 == 0)
        {
            write(1, "buzz\n", 5);
        }
        i++;
        putnbr(i);
        write(1, "\n", 1);
    }
    return (0);
}
