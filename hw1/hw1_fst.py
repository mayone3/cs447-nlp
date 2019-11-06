from fst import *

# here are some predefined character sets that might come in handy.
# you can define your own
AZ = set("abcdefghijklmnopqrstuvwxyz")
VOW = set("aeiou")
CONS = set("bcdfghjklmnprstvwxyz")
AO = set("ao")
E = set("e")
I = set("i")
U = set("u")
Y = set("y")
NR = set("nr")
PT = set("pt")
NPTR = set("nptr")


# Implement your solution here
def buildFST():
    print("Your task is to implement a better FST in the buildFST() function, using the methods described here")
    print("You may define additional methods in this module (hw1_fst.py) as desired")
    #
    # The states (you need to add more)
    # ---------------------------------------
    #
    f = FST("q0") # q0 is the initial (non-accepting) state

    f.addState("q1_cons")
    f.addState("q1_ao")
    f.addState("q1_e")
    f.addState("q1_i")
    f.addState("q1_u")

    f.addState("q1_ao_v2")
    f.addState("q1_e_v2")
    f.addState("q1_i_v2")
    f.addState("q1_u_v2")

    f.addState("q1_nn")
    f.addState("q1_pp")
    f.addState("q1_tt")
    f.addState("q1_rr")
    f.addState("q1_ie")

    f.addState("q_ing") # a non-accepting state
    f.addState("q_EOW", True) # an accepting state (you shouldn't need any additional accepting states)

    #
    # The transitions (you need to add more):
    # ---------------------------------------
    # transduce every element in this set to itself:
    f.addSetTransition("q0", AO, "q1_ao")
    f.addSetTransition("q0", E, "q1_e")
    f.addTransition("q0", "i", "", "q1_i")
    f.addSetTransition("q0", U, "q1_u")
    f.addSetTransition("q0", CONS, "q1_cons")

    # q1_cons
    f.addSetTransition("q1_cons", AO, "q1_ao")
    f.addSetTransition("q1_cons", E, "q1_e")
    f.addTransition("q1_cons", "i", "", "q1_i")
    f.addSetTransition("q1_cons", U, "q1_u")
    f.addSetTransition("q1_cons", CONS, "q1_cons")

    f.addSetTransition("q1_cons", AZ-E, "q_ing")
    f.addTransition("q1_cons", "e", "", "q_ing")

    # q1_ao
    f.addSetTransition("q1_ao", AO, "q1_ao_v2")
    f.addSetTransition("q1_ao", E, "q1_e_v2")
    f.addSetTransition("q1_ao", I, "q1_i_v2")
    f.addSetTransition("q1_ao", U, "q1_u_v2")
    f.addSetTransition("q1_ao", CONS-NPTR, "q1_cons")
    f.addTransition("q1_ao", "n", "n", "q1_nn")
    f.addTransition("q1_ao", "p", "p", "q1_pp")
    f.addTransition("q1_ao", "t", "t", "q1_tt")
    f.addTransition("q1_ao", "r", "r", "q1_rr")
    f.addSetTransition("q1_ao", AZ-NPTR, "q_ing")

    # q1_e
    f.addSetTransition("q1_e", AO, "q1_ao_v2")
    f.addSetTransition("q1_e", E, "q1_e_v2")
    f.addSetTransition("q1_e", I, "q1_i_v2")
    f.addSetTransition("q1_e", U, "q1_u_v2")
    f.addSetTransition("q1_e", CONS-PT, "q1_cons")
    f.addTransition("q1_e", "p", "p", "q1_pp")
    f.addTransition("q1_e", "t", "t", "q1_tt")
    f.addSetTransition("q1_e", AZ-PT, "q_ing")

    # q1_i
    f.addTransition("q1_i", "a", "ia", "q1_ao_v2")
    f.addTransition("q1_i", "b", "ib", "q1_cons")
    f.addTransition("q1_i", "c", "ic", "q1_cons")
    f.addTransition("q1_i", "d", "id", "q1_cons")
    f.addTransition("q1_i", "e", "", "q1_ie")
    f.addTransition("q1_i", "f", "if", "q1_cons")
    f.addTransition("q1_i", "g", "ig", "q1_cons")
    f.addTransition("q1_i", "h", "ih", "q1_cons")
    f.addTransition("q1_i", "i", "ii", "q1_i_v2")
    f.addTransition("q1_i", "j", "ij", "q1_cons")
    f.addTransition("q1_i", "k", "ik", "q1_cons")
    f.addTransition("q1_i", "l", "il", "q1_cons")
    f.addTransition("q1_i", "m", "im", "q1_cons")
    f.addTransition("q1_i", "n", "in", "q1_nn")
    f.addTransition("q1_i", "o", "io", "q1_ao_v2")
    f.addTransition("q1_i", "p", "ip", "q1_pp")
    f.addTransition("q1_i", "q", "iq", "q1_cons")
    f.addTransition("q1_i", "r", "ir", "q1_rr")
    f.addTransition("q1_i", "s", "is", "q1_cons")
    f.addTransition("q1_i", "t", "it", "q1_tt")
    f.addTransition("q1_i", "u", "iu", "q1_u_v2")
    f.addTransition("q1_i", "v", "iv", "q1_cons")
    f.addTransition("q1_i", "w", "iw", "q1_cons")
    f.addTransition("q1_i", "x", "ix", "q1_cons")
    f.addTransition("q1_i", "y", "iy", "q1_cons")
    f.addTransition("q1_i", "z", "iz", "q1_cons")

    #f.addSetTransition("q1_i", AZ-NPTR-E, "q_ing")
    f.addTransition("q1_i", "a", "ia", "q_ing")
    f.addTransition("q1_i", "b", "ib", "q_ing")
    f.addTransition("q1_i", "c", "ic", "q_ing")
    f.addTransition("q1_i", "d", "id", "q_ing")
    f.addTransition("q1_i", "f", "if", "q_ing")
    f.addTransition("q1_i", "g", "ig", "q_ing")
    f.addTransition("q1_i", "h", "ih", "q_ing")
    f.addTransition("q1_i", "i", "ii", "q_ing")
    f.addTransition("q1_i", "j", "ij", "q_ing")
    f.addTransition("q1_i", "k", "ik", "q_ing")
    f.addTransition("q1_i", "l", "il", "q_ing")
    f.addTransition("q1_i", "m", "im", "q_ing")
    f.addTransition("q1_i", "o", "io", "q_ing")
    f.addTransition("q1_i", "q", "iq", "q_ing")
    f.addTransition("q1_i", "s", "is", "q_ing")
    f.addTransition("q1_i", "u", "iu", "q_ing")
    f.addTransition("q1_i", "v", "iv", "q_ing")
    f.addTransition("q1_i", "w", "iw", "q_ing")
    f.addTransition("q1_i", "x", "ix", "q_ing")
    f.addTransition("q1_i", "y", "iy", "q_ing")
    f.addTransition("q1_i", "z", "iz", "q_ing")

    # q1_u
    f.addSetTransition("q1_u", AO, "q1_ao_v2")
    f.addSetTransition("q1_u", E, "q1_e_v2")
    f.addSetTransition("q1_u", I, "q1_i_v2")
    f.addSetTransition("q1_u", U, "q1_u_v2")
    f.addSetTransition("q1_u", CONS-NPTR, "q1_cons")
    f.addTransition("q1_u", "n", "n", "q1_nn")
    f.addTransition("q1_u", "p", "p", "q1_pp")
    f.addTransition("q1_u", "t", "t", "q1_tt")
    f.addTransition("q1_u", "r", "r", "q1_rr")
    f.addSetTransition("q1_u", AZ-E-NPTR, "q_ing")
    f.addTransition("q1_u", "e", "", "q_ing")

    # q1_*_v2
    f.addSetTransition("q1_ao_v2", AO, "q1_ao_v2")
    f.addSetTransition("q1_ao_v2", E, "q1_e_v2")
    f.addSetTransition("q1_ao_v2", I, "q1_i_v2")
    f.addSetTransition("q1_ao_v2", U, "q1_u_v2")
    f.addSetTransition("q1_ao_v2", CONS, "q1_cons")
    f.addSetTransition("q1_ao_v2", AZ, "q_ing")

    f.addSetTransition("q1_e_v2", AO, "q1_ao_v2")
    f.addSetTransition("q1_e_v2", E, "q1_e_v2")
    f.addSetTransition("q1_e_v2", I, "q1_i_v2")
    f.addSetTransition("q1_e_v2", U, "q1_u_v2")
    f.addSetTransition("q1_e_v2", CONS, "q1_cons")
    f.addSetTransition("q1_e_v2", AZ, "q_ing")

    f.addSetTransition("q1_i_v2", AO, "q1_ao_v2")
    f.addTransition("q1_i_v2", "e", "", "q1_ie")
    f.addSetTransition("q1_i_v2", I, "q1_i_v2")
    f.addSetTransition("q1_i_v2", U, "q1_u_v2")
    f.addSetTransition("q1_i_v2", CONS, "q1_cons")
    f.addSetTransition("q1_i_v2", AZ, "q_ing")

    f.addSetTransition("q1_u_v2", AO, "q1_ao_v2")
    f.addSetTransition("q1_u_v2", E, "q1_e_v2")
    f.addSetTransition("q1_u_v2", I, "q1_i_v2")
    f.addSetTransition("q1_u_v2", U, "q1_u_v2")
    f.addSetTransition("q1_u_v2", CONS, "q1_cons")
    f.addSetTransition("q1_u_v2", AZ-E, "q_ing")
    f.addTransition("q1_u_v2", "e", "", "q_ing")

    # q1_ie
    f.addTransition("q1_ie", "", "y", "q_ing")
    f.addTransition("q1_ie", "a", "iea", "q1_ao_v2")
    f.addTransition("q1_ie", "b", "ieb", "q1_cons")
    f.addTransition("q1_ie", "c", "iec", "q1_cons")
    f.addTransition("q1_ie", "d", "ied", "q1_cons")
    f.addTransition("q1_ie", "e", "iee", "q1_e_v2")
    f.addTransition("q1_ie", "f", "ief", "q1_cons")
    f.addTransition("q1_ie", "g", "ieg", "q1_cons")
    f.addTransition("q1_ie", "h", "ieh", "q1_cons")
    f.addTransition("q1_ie", "i", "iei", "q1_i_v2")
    f.addTransition("q1_ie", "j", "iej", "q1_cons")
    f.addTransition("q1_ie", "k", "iek", "q1_cons")
    f.addTransition("q1_ie", "l", "iel", "q1_cons")
    f.addTransition("q1_ie", "m", "iem", "q1_cons")
    f.addTransition("q1_ie", "n", "ien", "q1_cons")
    f.addTransition("q1_ie", "o", "ieo", "q1_ao_v2")
    f.addTransition("q1_ie", "p", "iep", "q1_cons")
    f.addTransition("q1_ie", "q", "ieq", "q1_cons")
    f.addTransition("q1_ie", "r", "ier", "q1_cons")
    f.addTransition("q1_ie", "s", "ies", "q1_cons")
    f.addTransition("q1_ie", "t", "iet", "q1_cons")
    f.addTransition("q1_ie", "u", "ieu", "q1_u_v2")
    f.addTransition("q1_ie", "v", "iev", "q1_cons")
    f.addTransition("q1_ie", "w", "iew", "q1_cons")
    f.addTransition("q1_ie", "x", "iex", "q1_cons")
    f.addTransition("q1_ie", "y", "iey", "q1_cons")
    f.addTransition("q1_ie", "z", "iez", "q1_cons")

    # q1_nn
    f.addTransition("q1_nn", "", "n", "q_ing")
    f.addSetTransition("q1_nn", AO, "q1_ao")
    f.addSetTransition("q1_nn", E, "q1_e")
    f.addTransition("q1_nn", "i", "", "q1_i")
    f.addSetTransition("q1_nn", U, "q1_u")
    f.addSetTransition("q1_nn", CONS, "q1_cons")
    f.addSetTransition("q1_nn", AZ-E, "q_ing")
    f.addTransition("q1_nn", "e", "", "q_ing")

    # q1_pp
    f.addTransition("q1_pp", "", "p", "q_ing")
    f.addSetTransition("q1_pp", AO, "q1_ao")
    f.addSetTransition("q1_pp", E, "q1_e")
    f.addTransition("q1_pp", "i", "", "q1_i")
    f.addSetTransition("q1_pp", U, "q1_u")
    f.addSetTransition("q1_pp", CONS, "q1_cons")
    f.addSetTransition("q1_pp", AZ-E, "q_ing")
    f.addTransition("q1_pp", "e", "", "q_ing")

    # q1_tt
    f.addTransition("q1_tt", "", "t", "q_ing")
    f.addSetTransition("q1_tt", AO, "q1_ao")
    f.addSetTransition("q1_tt", E, "q1_e")
    f.addTransition("q1_tt", "i", "", "q1_i")
    f.addSetTransition("q1_tt", U, "q1_u")
    f.addSetTransition("q1_tt", CONS, "q1_cons")
    f.addSetTransition("q1_tt", AZ-E, "q_ing")
    f.addTransition("q1_tt", "e", "", "q_ing")

    # q1_rr
    f.addTransition("q1_rr", "", "r", "q_ing")
    f.addSetTransition("q1_rr", AO, "q1_ao")
    f.addSetTransition("q1_rr", E, "q1_e")
    f.addTransition("q1_rr", "i", "", "q1_i")
    f.addSetTransition("q1_rr", U, "q1_u")
    f.addSetTransition("q1_rr", CONS, "q1_cons")
    f.addSetTransition("q1_rr", AZ-E, "q_ing")
    f.addTransition("q1_rr", "e", "", "q_ing")

    # map the empty string to ing:
    f.addTransition("q_ing", "", "ing", "q_EOW")

    # Return your completed FST
    # f.printFST()
    return f


if __name__ == "__main__":
    # Pass in the input file as an argument
    if len(sys.argv) < 2:
        print("This script must be given the name of a file containing verbs as an argument")
        quit()
    else:
        file = sys.argv[1]
    #endif

    # Construct an FST for translating verb forms
    # (Currently constructs a rudimentary, buggy FST; your task is to implement a better one.
    f = buildFST()
    # Print out the FST translations of the input file
    f.parseInputFile(file)
