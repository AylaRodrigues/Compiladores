# 🧊 COOL Compiler (Python Implementation)

> A complete compiler for the **COOL** (Class Object Oriented Language) programmed in **Python**, featuring lexical, syntactic, and semantic analysis.

---

## 📌 Project Overview

This repository contains the source code for the **COOL** compiler. The goal of this project is to transform COOL source code into a structured, validated intermediate representation by strictly enforcing language grammar and logical rules.

### 🏗️ Compiler Pipeline

The compilation process is divided into three fundamental phases:

1. **Lexical Analysis (Scanner):** Converts the raw character stream into a sequence of meaningful **Tokens**, handling COOL-specific features like nested comments and string escapes.
2. **Syntactic Analysis (Parser):** Validates the token sequence against the COOL grammar, generating an **Abstract Syntax Tree (AST)**.
3. **Semantic Analysis:** Performs logical validation, including **Type Checking** (Least Upper Bound, Dispatch validation), **Scope Management**, and **Inheritance Graph Validation**.

---

## 🚀 Key Features

* **Python-Powered:** Built with Python 3.x for maximum readability and maintainability.
* **Full COOL Grammar:** Supports classes, inheritance, and strongly-typed expressions.
* **Robust Error Reporting:** Detailed messages for syntax and semantic errors.
* **Symbol Table:** Efficient management of method and attribute scopes across class hierarchies.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Parsing:** [Ex: PLY / SLY / Custom]
* **Testing:** COOL Test Suite (.cl files)

---

### Made by Ayla Rodrigues e Sofia Kitaeva 
[![Github](https://img.shields.io/badge/-Ayla-%23121011?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AylaRodrigues)
[![Github](https://img.shields.io/badge/-Sofia-%23121011?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SofiaKitaeva)
