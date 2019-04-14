#include <iostream>
#include <string>

std::string s;
int i = -1;
char token;

void E();
void T();
void R();
void S();
void check(std::string alpha);
void parse_nonterminal(std::string alpha);

std::string first(char c) {
  switch(c) {
    case '$': return std::string("$"); break;
    case '+': return std::string("+"); break;
    case '*': return std::string("*"); break;
    case 'l': return std::string("l"); break;
    case '(': return std::string("("); break;
    case ')': return std::string(")"); break;
    case 'n': return std::string("n"); break;
    case 'E': return std::string("n("); break;
    case 'T': return std::string("n("); break;
    case 'R': return std::string("+*l"); break;
    case 'S': return std::string("n("); break;
  }
}

std::string follow(char c) {
  switch(c) {
    case '$': return std::string("$"); break;
    case '+': return std::string("n("); break;
    case '*': return std::string("n("); break;
    case 'l': return std::string(")$"); break;
    case '(': return std::string("n("); break;
    case ')': return std::string("+l*"); break;
    case 'n': return std::string("+l*"); break;
    case 'E': return std::string(")$"); break;
    case 'T': return std::string("+l*"); break;
    case 'R': return std::string(")$"); break;
    case 'S': return std::string("$"); break;
  }
}

char scan() {
  ++i;
  if (i < s.size()) {
    return s[i];
  }
  return EOF;
}

void check_terminal(std::string alpha) {
  if (alpha[0] == token) {
    token = scan();
  }
  else {
    std::cout << alpha[0] + " expected\n";
  }
  if (alpha.size() >= 2) {
    check(alpha.substr(1));
  }
}

void check_nonterminal(std::string alpha) {
  parse_nonterminal(alpha);
}

void check(std::string alpha) {
  switch(alpha[0]) {
    case '$': check_terminal(alpha); break;
    case '+': check_terminal(alpha); break;
    case '*': check_terminal(alpha); break;
    case 'l': check_terminal(alpha); break;
    case '(': check_terminal(alpha); break;
    case ')': check_terminal(alpha); break;
    case 'n': check_terminal(alpha); break;
    case 'E': check_nonterminal(alpha); break;
    case 'T': check_nonterminal(alpha); break;
    case 'R': check_nonterminal(alpha); break;
    case 'S': check_nonterminal(alpha); break;
  }
}

void parse_terminal(std::string alpha) {
  if (alpha[0] != 'l') {
    token = scan();
  }
  if (alpha.size() >= 2) {
    check(alpha.substr(1));
  }
}

void parse_nonterminal(std::string alpha) {
  switch(alpha[0]) {
    case 'E':E(); break;
    case 'T':T(); break;
    case 'R':R(); break;
    case 'S':S(); break;
  }
  if (alpha.size() >= 2) {
    check(alpha.substr(1));
  }
}

void E() {
  if (first('T').find(token) != std::string::npos) {
    std::cout << "E -> TR\n";
    parse_nonterminal("TR");
    return;
  }
  std::cout << "Se asteapta un token diferit\n";
}

void T() {
  if (first('(').find(token) != std::string::npos) {
    std::cout << "T -> (E)\n";
    parse_terminal("(E)");
    return;
  }
  if (first('n').find(token) != std::string::npos) {
    std::cout << "T -> n\n";
    parse_terminal("n");
    return;
  }
  std::cout << "Se asteapta un token diferit\n";
}

void R() {
  if (first('+').find(token) != std::string::npos) {
    std::cout << "R -> +TR\n";
    parse_terminal("+TR");
    return;
  }
  if (first('*').find(token) != std::string::npos) {
    std::cout << "R -> *TR\n";
    parse_terminal("*TR");
    return;
  }
  if (follow('R').find(token) != std::string::npos) {
    std::cout << "R -> l\n";
    parse_terminal("l");
    return;
  }
  std::cout << "Se asteapta un token diferit\n";
}

void S() {
  if (first('E').find(token) != std::string::npos) {
    std::cout << "S -> E$\n";
    parse_nonterminal("E$");
    return;
  }
  std::cout << "Se asteapta un token diferit\n";
}

int main() {
  std::cin >> s;
  token = scan();
  S();
  if (token != EOF) {
      std::cout << "ERROR: EOF expectd\n";
  }
  return 0;
}
