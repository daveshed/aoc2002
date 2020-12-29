#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

typedef struct {
    long long int remainder;
    long long int base;
} modulo_t;


// FIX: basic stuff should go in a generic utils
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

/*
 * Read ints from a comma separated string - doesn't handle spaces. If a value
 * cannot be parsed to an int then push a 0 into the vector.
 */
std::vector<int> read_ints(std::stringstream ss)
{
    std::vector<int> result;
    while (ss.good())
    {
        std::string substr;
        getline(ss, substr, ',');
        try
        {
            result.push_back(std::stoi(substr, nullptr));
        }
        catch (std::invalid_argument)
        {
            result.push_back(0);
        }
    }
    return result;
}

#if 0
/*
 * Get the greatest common divisor via the extended Euclidean algorithm
 */
int get_gcd_extended(
    long long int a, long long int b, long long int* x, long long int* y)
{
    // remainder is 0 so terminate
    if (a == 0)
    {
        *x = 0, *y = 1;
        return b;
    }
    // To store results of recursive call
    long long int x1 = 0;
    long long int y1 = 0;
    int gcd = get_gcd_extended(b % a, a, &x1, &y1);
    // Update x and y using results of recursive call
    *x = y1 - (b / a) * x1;
    *y = x1;
    return gcd;
}

// Function to find modulo inverse of `a`
long long int get_mod_inverse(long long int a, long long int m)
{
    long long int x = 0;
    long long int y = 0;
    int g = get_gcd_extended(a, m, &x, &y);
    if (g != 1)
    {
        throw std::runtime_error(
            "Inverse doesn't exist for "
            + std::to_string(a)
            + " mod "
            + std::to_string(m));
    }
    // m is added to handle negative x
    return (x % m + m) % m;
}
#endif
long long int get_mod_inverse(long long int a, long long int m)
{
    long long int m0 = m;
    long long int y = 0, x = 1;

    if (m == 1)
        return 0;

    while (a > 1) {
        // q is quotient
        long long int q = a / m;
        long long int t = m;

        // m is remainder now, process same as
        // Euclid's algo
        m = a % m, a = t;
        t = y;

        // Update y and x
        y = x - q * y;
        x = t;
    }

    // Make x positive
    if (x < 0)
        x += m0;

    return x;
}


/*
 * Simultaneous modular equation solver via Chinese remainder theorem. Given...
 * (1) x => r_1 (mod m_1)
 * (2) x => r_2 (mod m_2)
 * the solver will return x as a remainder with its modulo base.
*/
modulo_t solve_simultaneous_modular(modulo_t eqn1, modulo_t eqn2)
{
    long long int remainder = \
        (eqn2.remainder - eqn1.remainder) \
        * get_mod_inverse(eqn1.base, eqn2.base) * eqn1.base \
        + eqn1.remainder;
    // make sure the remainder is positive and less than base...
    long long int base = eqn1.base * eqn2.base;
    remainder %= base;
    remainder = (remainder < 0) ? (base + remainder) : remainder;
    return (modulo_t){remainder, base};
}

/*
 * Takes your given time and returns how many minutes you will have to wait
 * until a given bus id departs.
 */
long long int ticks_to_wait(long long int time, int bus_id)
{
    assert(bus_id);
    assert(time);
    long long int missed_bus_by = time % bus_id;
    assert(missed_bus_by >= 0);
    if (missed_bus_by == 0) // you're on time!
    {
        return 0;
    }
    return bus_id - missed_bus_by; // need to wait
}

/*
 * Looks through the timetable for the next bus to depart from the time you've
 * specified.
*/
int get_next_bus(unsigned long long int time, std::vector<int> buses)
{
    int next_bus = buses[0];
    unsigned long long int min_wait = ticks_to_wait(time, next_bus);
    for (
        std::vector<int>::iterator bus = buses.begin();
        bus != buses.end();
        ++bus)
    {
        if (!*bus)
        {
            continue;
        }
        long long int wait = ticks_to_wait(time, *bus);
        if (wait < min_wait)
        {
            next_bus = *bus;
            min_wait = wait;
        }
    }
    return next_bus;
}

/*
 * Returns true if all the buses in the timetable depart in sequence according
 * to their index in the vector each on the minute every minute.
*/
bool buses_depart_in_sequence(
    long long int departure, std::vector<int>& buses)
{
    assert(departure);
    for (int idx = 0; idx < buses.size(); idx++)
    {
        // ignore 0 bus ids - these will come from 'x' in the timetable
        if (!buses[idx])
        {
            continue;
        }
        // Each bus must depart after bus idx 0 by idx minutes...
        if (ticks_to_wait(departure, buses[idx]) != idx)
        {
            std::cout << "bus " << buses[idx] << " out of sequence" << std::endl;
            return false;
        }
    }
    return true;
}

// look up the next bus in the timetable by index ignoring 0's.
bool read_timetable(
    const std::vector<int>& buses, int& idx, modulo_t& result)
{
    while (idx < buses.size())
    {
        int bus = buses[idx];
        if (bus)
        {
            result.remainder = -1 * idx; // need to move to the RHS
            result.base = bus;
            return true;
        }
        idx++;
    }
    return false;
}

std::string show_modulo(modulo_t x)
{
    return (
        "x => " + std::to_string(x.remainder)
        + " mod " + std::to_string(x.base));
}

/*
 * Get the departure time where each bus in the timetable departs in sequence
 * on the minute every minute.
 */
long long int get_solution_part2(std::vector<int>& buses)
{
    /* Consume the bus timetable one at a time ie. take bus_0 and bus_1 and get
    a new relationship for departure time. Then consume this against bus_2 and
    so on...*/
    int idx = 0;
    // 1. get the first bus in the timetable...
    modulo_t eqn1;
    modulo_t eqn2;
    modulo_t result;
    read_timetable(buses, idx, eqn1);
    // 2. consume each bus in the timetable in turn...
    while (true)
    {
        idx++;
        if (!read_timetable(buses, idx, eqn2))
        {
            break;
        }
        result = solve_simultaneous_modular(eqn1, eqn2);
        std::cout << show_modulo(eqn1) << " with " \
            << show_modulo(eqn2) << " result... " \
            << show_modulo(result) << std::endl;
        eqn1 = result;
    }
    return result.remainder;
}

typedef struct {
    int departure;
    std::vector<int> bus_ids;
} my_notes_t;

my_notes_t parse(std::vector<std::string> lines)
{
    int departure = std::stoi(lines[0], nullptr);
    std::vector<int> buses = read_ints(std::stringstream(lines[1]));
    return (my_notes_t){departure, buses};
}

int main(void)
{
    // basic tests...
    assert(8 == ticks_to_wait(47, 11));
    assert(0 == ticks_to_wait(3417, 17));

    modulo_t eqn1 = {3, 5};
    modulo_t eqn2 = {4, 7};
    modulo_t result = solve_simultaneous_modular(eqn1, eqn2);
    assert(18 == result.remainder);
    assert(35 == result.base);


    // test against example input...
    std::ifstream input("input-example.txt");
    assert(input.is_open());
    my_notes_t notes = parse(read_lines(input));
    input.close();
    assert(59 == get_next_bus(notes.departure, notes.bus_ids));

    // now do the actual input...
    std::ifstream puzzle_input("input-day13.txt");
    assert(puzzle_input.is_open());
    notes = parse(read_lines(puzzle_input));
    puzzle_input.close();
    //
    // int next_bus = get_next_bus(notes.departure, notes.bus_ids);
    // unsigned long long int minutes = ticks_to_wait(notes.departure, next_bus);
    // std::cout << "Next bus " << next_bus << " leaving in " \
    //     << minutes << " mins" << std::endl;

    // part 2 test cases...
    std::cout << "##################  PART2  ##################" << std::endl;
    std::cout << "TEST1..." << std::endl;
    std::vector<int> fake_timetable1{7, 13, 0, 0, 59, 0, 31, 19};
    assert(1068781 == get_solution_part2(fake_timetable1));
    assert(buses_depart_in_sequence(1068781, fake_timetable1));
    std::cout << "TEST2..." << std::endl;
    std::vector<int> fake_timetable2{17, 0, 13, 19};
    assert(3417 == get_solution_part2(fake_timetable2));
    assert(buses_depart_in_sequence(3417, fake_timetable2));
    std::cout << "TEST3..." << std::endl;
    std::vector<int> fake_timetable3{67, 7, 59, 61};
    assert(754018 == get_solution_part2(fake_timetable3));
    std::cout << "TEST4..." << std::endl;
    std::vector<int> fake_timetable4{67, 0, 7, 59, 61};
    assert(779210 == get_solution_part2(fake_timetable4));
    std::cout << "TEST5..." << std::endl;
    std::vector<int> fake_timetable5{67, 7, 0, 59, 61};
    assert(1261476 == get_solution_part2(fake_timetable5));
    std::cout << "TEST6..." << std::endl;
    std::vector<int> fake_timetable6{1789, 37, 47, 1889};
    assert(1202161486 == get_solution_part2(fake_timetable6));

    // part 2 solution...
    std::cout << "SOLUTION..." << std::endl;
    long long int part2_solution = get_solution_part2(notes.bus_ids);
    assert(buses_depart_in_sequence(part2_solution, notes.bus_ids));

    std::cout << "Part 2 departure time " << part2_solution \
        << " minutes" << std::endl;

    return 0;
}