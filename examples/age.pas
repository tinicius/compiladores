program Greeting;

var
  name: string;
  age, nextAge: integer;

begin

  name:= "emanuel";

  write("Enter your age: ");
  readln(age);

  nextAge := age + 1;

  writeln("Hello, ", name, "!");
  writeln("Next year, you will be ", nextAge, " years old.");

end.
