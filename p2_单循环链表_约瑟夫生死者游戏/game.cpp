/*
题目二	约瑟夫生者死者游戏

项目简介
	约瑟夫生者死者游戏的大意是：30个旅客同乘一条船，因为严重超载，加上风高浪大危险万分；因此船长告诉乘客，只有将全船一半的旅客投入海中，其余人才能幸免于难。无奈，大家只得统一这种方法，并议定30个人围成一圈，由第一个人开始，依次报数，数到第9人，便将他投入大海中，然后从他的下一个人数起，数到第9人，再将他投入大海，如此循环，直到剩下15个乘客为止。问哪些位置是将被扔下大海的位置。

项目功能要求：(要求采用单循环链表)
	本游戏的数学建模如下：假如N个旅客排成一个环形，依次顺序编号1, 2, …, N。从某个指定的第S号开始。沿环计数，每数到第M个人就让器出列，且从下一个人开始重新计数，继续进行下去。这个过程一直进行到剩下K个旅客为止。
	本游戏要求用户输入的内容包括：
1、 旅客的个数，也就是N的值；
2、 离开旅客的间隔书，也就是M的值；
3、 所有旅客的序号作为一组数据要求存放在某种数据结构中。
本游戏要求输出的内容是包括：
1. 离开旅客的序号；
2. 剩余旅客的序号。
*/

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <iterator>
#include <vector>

using namespace std;

class Person
{
public:
	int id;
	Person* next;
	int alive = 1;
	Person(int _id) : id(_id){
	}
	void link(Person* _next){
		next = _next;
	}

};

class Circle
{
public:
	int length;
	Person* head;
	Circle(int _length) : length(_length){
		auto prev = new Person(1);
		Person* p_ptr;
		head = prev;
		prev->link(prev);
		for (int i = 2; i <= length; ++i)
		{
			p_ptr = new Person(i);
			prev->link(p_ptr);
			prev = p_ptr;
		}
		p_ptr->link(head);
		// auto p = head;
		// for (int i = 1; i <= length; ++i)
		// {
		// 	cout << p << "=>" << p->next << "\t";
		// 	p = p->next;
		// }
	}
	void start(int start_id, int rounds, int gap){
		auto start_p = head;
		auto p = head;
		while (true) {
			if (start_p->id == start_id)
				break;
			start_p = start_p->next;
		}
		while (rounds--){
			start_p = count(start_p, gap-1);
		}
		p = head;
		if (p->alive)
			cout << "alive: " << p->id << "\t";
		p = p->next;
		while (p!=head){
			if (p->alive)
			cout << p->id << "\t";
			p = p->next;
		}
		cout << endl;
	}
	Person* count(Person* start_p, int gap){
		while (gap--){
			if (start_p->alive == 0) {
				gap++;
			}
			start_p = start_p->next;
		}
		while (start_p->alive == 0){
			start_p = start_p->next;
		}
		start_p->alive = 0;
		cout << "dead: " << start_p->id << endl;
		return start_p;
	}
};

int main(int argc, char const *argv[])
{
	int total;
	int start_id;
	int gap;
	int to_die;
	cout << "input total num:" << endl;
	cin >> total;
	cout << "input start id: " << endl;
	cin >> start_id;
	cout << "input death num: " << endl;
	cin >> gap;
	cout << "input how many to die" << endl;
	cin >> to_die;
	auto circle = Circle(total);
	circle.start(start_id, to_die, gap);
	return 0;
}