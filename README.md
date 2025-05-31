<a name="readme-top"></a>

<div align="center">
  <h3 align="center">Cinder</h3>
  <p align="center">
    A simple rust-like programming language.
    <br />
    <br />
  </p>
</div>


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#command-line-options">Command Line Options</a></li>
        <li><a href="#syntax">Syntax</a></li>
          <ul>
            <li><a href="#functions">Functions</a></li>
            <li><a href="#types">Types</a></li>
            <li><a href="#statements">Statements</a></li>
            <li><a href="#control-flow">Control Flow</a></li>
            <li><a href="#comments">Comments</a></li>
          </ul>
      </ul>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## About The Project
`Cinder` is a more in-depth programming language than my previous attempt, [Peanut Butter](https://github.com/PeanutButterRat/peanut-butter). It has a Rust-like syntax and supports basic control flow with functions and if-statements. `Cinder` has just the bare essentials to make some basic programs, but is a good starting point for further extensions and improvements. I originally planned on having many more features, but got preoccupied with other responsibilities and decided to leave it in the state that it was in considering it was a good place to leave off.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

### Prerequisites

`Cinder` uses [Poetry](https://python-poetry.org/) for package management, so you should follow the installation steps [here](https://python-poetry.org/docs/#installation) in order to get started.

### Installation

After Poetry is up and running,

1. Clone the repository:
   ```sh
   git clone https://github.com/PeanutButterRat/cinder.git
   cd cinder  # You should now be in the project directory.
   ```

2. Install `Cinder`:
   ```sh
   poetry install
   ```

3. You can now run poetry with...
   ```sh
   poetry run cinder <source>
   ```

Now you are good to go!

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

```sh
poetry run cinder <source>
```

After compiling, the resulting executable can be found at `/build/output.exe`.

### Command Line Options
Here is a short table of options supported by the compiler (mostly for compiler debugging purposes):

| Option    | Long Form       | Description                                                            |
|-----------|-----------------|------------------------------------------------------------------------|
| -h        | --help          | Displays the help menu.                                                |
| -a        | --show-ast      | Shows the abstract syntax tree (AST) before attempting to compile.     |
| -s        | --stack-trace   | Displays the stack trace if an exception is raised during compilation. |
| -t TARGET | --target TARGET | Set the compilation target. TARGET should be a standard target triple. |
| -d        | --dump-assembly | Prints the LLVM assembly module before compiling.                      |

### Syntax
The following section details the grammatical rules for using `Cinder`.

#### Functions
Every `Cinder` program must have a `main` function, just like other C-type languages. To declare a function use the following form:
```
fn function(param-1: type, param-2: type, etc. ) -> return-type {
    function body goes here
}
```
As in...
```
fn main() -> i32 {
    let sequence: i32 = fib(10);
    print sequence;
    return 0;
}

fn fib(n: i32) -> i32 {
    if n <= 1 {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}
```

#### Types
The only two types available in `Cinder` are integers and booleans in the form of `i32` and `bool` respectively. As a result of this limitation, functions **must** return either an integer or boolean (void is unsupported).

> [!IMPORTANT]
> If you encounter an LLVM error along the lines of `error: expected instruction opcode`, it most likely means you are missing a return statement somewhere.

#### Statements
The two types of statements that `Cinder` supports are assignment and `print`. To declare a variable use the following form:
```
let variable: type = value;
```
As in...
```
let a: i32 = 3;
let a: i32 = 4;  // Shadows the previous declaration.
```

You can also print values or string literals with `print`:
```
let a: i32 = 5;
print a;                  // Prints '5'.
print "a is equal to 5";  // Prints 'a is equal to 5'.
```

For logical expressions, the standard operators apply (`>`, `>=`, `<`, `<=`, `!=`, `==`) alongside `and`, `or`, and `not` for compound expressions.
```
let b: bool = 4 <= 5;  // b is set to true.
if b {
    print "b is true";
}
```

#### Control Flow
The only control flow structure that `Cinder` supports is the humble if-statement. Syntactically, it's a sort of a mix of Rust and Python:
```sh
if expression {
    do something here...
} elif expression {
    do something different here...
} else {
    do something else here...
}
```
Like so...
```
let a: i32 = 4;
if a > 3 {
  print "4 is indeed greater than 3.";
} else {
  print "EVERYBODY PANIC!";
}
```

#### Comments
Comments are declared using `//`. Block comments are unsupported.
```
// This is a comment.
// This is another comment.
```

This covers the main language features. As you can probably tell, it's not a super in-depth language. However, it has the basic features and is fairly easy to extend if you needed something to waste an afternoon on.

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
