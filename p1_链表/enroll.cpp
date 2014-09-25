/*
题目一  考试报名系统

项目简介：
	考试报名工作给各高校报名工作带来了新的挑战，给教务管理部门增加了很大的工作量。本项目是对考试报名管理的简单模拟，用控制台选项的选择方式完成下列功能：输入考生信息；输出考生信息；查询考生信息；添加考生信息；修改考生信息；删除考生信息。

项目功能要求：
本项目的实质是完成对考生信息的建立，查找，插入，修改，删除等功能。其中考生信息包括准考证号，姓名，性别，年龄和报考类别等信息。项目在设计时应首先确定系统的数据结构，定义类的成员变量和成员函数；然后实现各成员函数以完成对数据操作的相应功能；最后完成主函数以验证各个成员函数的功能并得到运行结果。（建议采用链表实现）
*/

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <iterator>
#include <vector>

using namespace std;
class Student
{
public:
	int id;
	string name;
	string gender;
	int age;
	string type;
	Student(string	init_string) {
		stringstream ss(init_string);
		ss >> id;
		ss >> name;
		ss >> gender;
		ss >> age;
		ss >> type;
	}
};
std::ostream& operator<<(std::ostream& outstream, Student& stu) {
		outstream << stu.id << "\t" << stu.name << "\t" << stu.gender << "\t" << stu.age << "\t" << stu.type;
	return outstream;
}

class LinkedNode
{
public:
	LinkedNode* previous = 0;
	Student* current = 0;
	LinkedNode* next = 0;
	LinkedNode (LinkedNode* _previous, Student* _current, LinkedNode* _next) : previous(_previous), current(_current), next(_next){
		// cout << "New Node:\n " <<
		// 		previous << "\t" << this << "\t" << next << endl;
	}
	~LinkedNode(){
		delete current;
		if (next)
			next->previous = previous;
		if (previous)
			previous->next = next;
	}
};

class LinkedList
{
public:
	LinkedNode* head;
	int length = 0;
	LinkedList(){
		head = 0;
	}
	~LinkedList(){
		while(head->next){
			auto current = head;
			head = head->next;
			delete current;
		}
	}
	int get_type(int location){
		auto p = head;
		bool tail = false;
		int type = 0;
		switch (1) {
			case 1:
				if (!p){ // empty list
					type = 0;
					break;
				}
				while (location--) {
					if (p->next) {
						p = p->next;
					} else {
						tail = true;  // insert at the tail;
						type = 2;
					}
				}
				if (!tail){  // insert before p. p is valide Node
					type = 1;
					break;
				}
		}
		return type;
	}
	LinkedNode* find(int stu_id){
		auto p = head;
		while ((p->current)->id != stu_id){
			p = p->next;
		}
		return p;
	}
	void remove(int location){
		auto p = head;
		while (location--) {
			p = p->next;
		}
		if (p==head)
			head = p->next;
		delete p;
	}
	void insert(Student* item, int location){
		auto p = head;
		bool tail = false;
		length++;
		int type = get_type(location);
		switch (type) {
			case 0: // empty list
			{	auto new_pointer = new LinkedNode(0, item, 0);
				head = new_pointer;
				return;
			}
			case 1:  // insert before p. p is valide Node
			{	auto new_pointer = new LinkedNode(p->previous, item, p);
				auto tmp = p->previous;
				p->previous = new_pointer;
				if (tmp) {
					tmp->next = new_pointer;
				} else { // new item becomes the head
					head = new_pointer;
				}
				break;
			}
			case 2: // insert at the tail;
			{	auto new_pointer = new LinkedNode(p, item, 0);
				p->next = new_pointer;
			}
		}
	}
};

void insert(ifstream& infile, LinkedList& students) {
	string line;
	int location = 0;
	cout << "input insert location, 0 for the head." << endl;
	getline(infile, line);
	location = stoi(line);
	cout << location << endl;
	cout << "input student data" << endl;
	cout << "id   name   gender   age    type" << endl;
	getline(infile, line);
	cout << line << endl;
	auto stu = new Student(line);
	students.insert(stu, location);
}

void print_list(LinkedList& students){
	auto p = students.head;
	while (p) {
		cout << *(p->current) << endl;
		// cout << p->previous << "\t" << p << "\t" << p->next << "\t";
		p = p->next;
	}
}

int get_int(ifstream& infile){
	string line;
	int id;
	getline(infile, line);
	id = stoi(line);
	cout << id << endl;
	return id;
}

int main(int argc, char const *argv[])
{
	// Student stu1("1 stu1 nv 19 sse");
	// cout << stu1;
	int num;
	string line;
	ifstream infile("test.in");
	cout << "input student num" << endl;
	num = get_int(infile);
	LinkedList students;
	while (num--) {
		insert(infile, students);
	}
	print_list(students);
	cout << "choose option: 1 insert      2 delete      3 find      4 edit      5 statics      0 exit" << endl;
	int opt,id;
	opt = get_int(infile);
	while (opt!=0) {
		switch (opt) {
			case 0:
				return 0;
			case 1:
				insert(infile, students);
				break;
			case 2:
				cout << "input delete id:" << endl;
				id = get_int(infile);
				delete students.find(id);
				break;
			case 3:
				cout << "input student id:" << endl;
				id = get_int(infile);
				cout << students.find(id)->current << endl;
				break;
			case 4:{
				cout << "input student id:" << endl;
				id = get_int(infile);
				delete students.find(id);
				cout << "input student data" << endl;
				cout << "id   name   gender   age    type" << endl;
				getline(infile, line);
				cout << line << endl;
				auto stu = new Student(line);
				students.insert(stu, 0);
				break;
			}
		}
		print_list(students);
		cout << "choose option: 1 insert      2 delete      3 find      4 edit       5statics      0 exit" << endl;
		getline(infile, line);
		opt = stoi(line);
		cout << opt << endl;

	}
	return 0;
}