program logic;

var
  x, y: integer;

begin
    y := x or x;
    y := x and x;
    y := not x;
    
    write(y);
end.