#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

// FIX: basic stuff should go in a generic utils
std::vector<std::string> read_lines(std::istream& input);

// A command after it's been parsed.
typedef struct Instruction {
    std::string type;
    int payload;
    bool executed;
} instruction_t;
/*
 * Emulates the console. You can give it the instructions and run them. It will
 * run until it sees an infinite loop then quit and you can get the accumulator
 * and the instruction that it was executing.
*/
class Console {
public:
    Console(std::vector<std::string>& raw_instructions);
    // Execute the instructions. Stop if an infinite loop is detected.
    void execute(void);
    // Retrieve the value of the accumulator
    int get_accumulator(void);
    // Get the next instruction
    instruction_t get_instruction(void);
private:
    std::vector<instruction_t> m_instructions;
    int m_accumulator;
    int m_stack_idx;

private:
    instruction_t parse(std::string& raw_instruction);
};

std::vector<std::string> read_lines(std::istream& input)
{
    std::vector<std::string> result;
    while (!input.eof())
    {
        std::string line;
        getline(input, line);
        result.push_back(line);
    }
    return result;
}

Console::Console(std::vector<std::string>& raw_instructions) :
    m_instructions()
{
    m_accumulator = 0;
    m_stack_idx = 0;
    for (
        auto to_parse = raw_instructions.begin();
        to_parse != raw_instructions.end();
        to_parse++)
    {
        m_instructions.push_back(parse(*to_parse));
    }
}

void Console::execute(void)
{
    std::cout << "Executing instructions..." << std::endl;
    while (m_stack_idx < m_instructions.size())
    {
        instruction_t& to_handle = m_instructions[m_stack_idx];
        if (to_handle.executed)
        {
            // already done this...
            break;
        }
        std::cout << "[" << m_stack_idx << "] handling..." << to_handle.type \
            << " -> " << to_handle.payload << std::endl;
        if (to_handle.type == "nop")
        {
            m_stack_idx++;
        }
        else if (to_handle.type == "acc")
        {
            m_accumulator += to_handle.payload;
            m_stack_idx++;
        }
        else if (to_handle.type == "jmp")
        {
            m_stack_idx += to_handle.payload;
        }
        else
        {
            throw std::runtime_error("Don't know what this command means");
        }
        // mark the instruction as executed...
        to_handle.executed = true;
    }
}

instruction_t Console::get_instruction(void)
{
    return m_instructions[m_stack_idx];
}

int Console::get_accumulator(void)
{
    return m_accumulator;
}

// PRIVATE
instruction_t Console::parse(std::string& raw_instruction)
{

    std::string type = raw_instruction.substr(0, 3);
    int payload = std::stoi(raw_instruction.substr(4), nullptr);
    return (instruction_t){type, payload, false};
}

int main(void)
{
    std::ifstream input("input-example.txt");
    assert(input.is_open());
    std::vector<std::string> boot_code = read_lines(input);
    Console console = Console(boot_code);
    console.execute();
    input.close();
    // Do the tests...
    // value of accumulator just before we execute an instruction for the second
    // time...
    assert(console.get_accumulator() == 5);
    // the instruction that we are going to re-execute...
    std::cout << console.get_instruction().type << std::endl;
    // assert(console.get_instruction().type == "jmp");
    return 0;
}
