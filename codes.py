class Codes:

    flow_codes = {
        0x0: 'return_subroutine',
        0x1: 'jump_subroutine',
        0x2: 'call_subroutine'
    }

    cond_codes = {
        0x3: 'skip_next_if_equal_address',
        0x4: 'skip_next_if_not_equal',
        0x5: 'skip_next_if_equal_register',
        0x9: 'skip_if_not_equal_register'
    }

    const_codes = {
        0x6: 'set_register',
        0x7: 'add_register'
    }

    assign = {
        0x0: 'set_register_equal'
    }

    bit_ops = {
        0x1: 'bitwise_or',
        0x2: 'bitwise_and',
        0x3: 'bitwise_xor',
        0x6: 'shift_right',
        0xE: 'shift_left'
    }

    math = {
        0x4: 'add_with_carry',
        0x5: 'substract_with_borrow',
        0x7: 'reversed_substraction'
    }

    mem = {
        0xA: 'set_i_to_address_plus'
    }

    rand = {
        0xC: 'set_bitwise_and_random',
        0xE: 'add_i_to_register',
        0x29: 'set_i_location_sprite',
    }

    most_significant_bit = (flow_codes, cond_codes, cond_codes)
    least_significant_bit = (math, bit_ops, mem)
