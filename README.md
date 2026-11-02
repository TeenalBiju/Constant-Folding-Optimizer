# ⚙️ FoldLab – Constant Folding Optimizer

A Python-based compiler optimization project that demonstrates **Constant Folding**, a technique used to simplify constant expressions during compile time.

FoldLab allows users to enter C-style source code, optimize arithmetic expressions, visualize the transformations, and compare the original source code with its optimized version through an interactive web interface.

## 📌 Project Overview

Constant Folding is a compiler optimization technique that evaluates expressions containing constant values at compile time and replaces them with their calculated results.

For example:

**Before Optimization**
```c
int a = 10 + 20;
int b = 5 * 4 + 2;
int c = (3 + 7) * 2;
int d = x + 6 * 3;
```

**After Optimization**
```c
int a = 30;
int b = 22;
int c = 20;
int d = x + 18;
```

The optimizer evaluates constant expressions while preserving variables whose values are unknown.

## ✨ Features

- **Interactive Code Editor:** Enter or modify C-style source code.
- **Sample Programs:** Choose from predefined examples.
- **Arithmetic Optimization:** Simplifies addition, subtraction, multiplication, division, modulo, and exponentiation where supported.
- **Nested Expression Folding:** Optimizes expressions containing multiple levels of parentheses.
- **Partial Constant Folding:** Simplifies constant subexpressions even when variables are present.
- **Comparison Optimization:** Evaluates supported constant comparison expressions.
- **Code Comparison:** Displays original and optimized source code side by side.
- **Optimization Trace:** Shows the transformations performed by the optimizer.
- **Optimization Statistics:** Displays folded expressions, changed lines, and source lines.
- **Download Optimized Code:** Export the optimized source text as a `.c` file.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core optimization logic |
| Streamlit | Interactive web interface |
| Python AST | Expression parsing and tree traversal |
| Operator Module | Arithmetic and comparison operations |
| Regular Expressions | Recognition of supported C-style statements |
| HTML and CSS | User interface styling |



## 🧠 How It Works

The optimizer follows a recursive expression-processing approach.

1. **Source Code Input:** The user enters source code or selects a sample program.
2. **Statement Recognition:** Supported C-style statements are identified using regular expressions.
3. **Expression Parsing:** Python's AST module parses the expressions into an Abstract Syntax Tree.
4. **Constant Detection:** The optimizer identifies expressions containing constant operands.
5. **Recursive Optimization:** Nested expressions are processed recursively.
6. **Constant Evaluation:** Eligible expressions are evaluated and replaced with their computed results.
7. **Output Generation:** The optimized source code and transformation logs are generated.
8. **Result Display:** The interface presents the optimized code, statistics, and optimization trace.

## 🧪 Example Optimization

**Input:**
```c
int result = (10 + 5) * 2;
int value = x + 4 * 3;
```

**Optimized Output:**
```c
int result = 30;
int value = x + 12;
```

The optimizer first evaluates the inner constant expressions and then simplifies the remaining expressions whenever possible.

## 📊 Application Workflow

```text
        Source Code Input
                |
                v
       Statement Recognition
                |
                v
         Expression Parsing
                |
                v
       Abstract Syntax Tree
                |
                v
       Constant Detection
                |
                v
       Recursive Folding
                |
                v
       Optimized Source Code
                |
                v
       Results and Statistics
```

## ⚠️ Limitations

- Supports a restricted subset of C-style source code, not the complete C language.
- Uses regular expressions for statement recognition.
- Does not perform constant propagation or dead-code elimination.
- Does not generate machine code or execute the resulting C program.
- Python arithmetic behaviour may differ from C arithmetic semantics in certain cases.

## 🎯 Project Objective

The main objective of FoldLab is to demonstrate the working of constant folding in compiler construction through an interactive application. It provides practical understanding of expression parsing, Abstract Syntax Trees, recursive processing, and compile-time optimization.

## 🔮 Future Scope

- Implement a complete lexer and parser for a defined C subset.
- Support more complex source-code structures.
- Introduce C-specific arithmetic and type handling.
- Add further compiler optimization techniques.
- Include automated test cases and optimization benchmarks.

## 👩‍💻 Project Information

**Project:** Constant Folding Optimizer (FoldLab)  
**Domain:** Compiler Construction  
**Language:** Python  
**Interface:** Streamlit  
**Optimization Technique:** Constant Folding



