from random import shuffle


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment.update({var: value})
                result = self.recursive_backtracking(assignment)
                if result is not False:
                    return result
                assignment.pop(var)
        return False

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_sa_csp():
    costa_rica = "Costa Rica"
    panama = "Panama"
    colombia = "Colombia"
    ecuador = "Ecuador"
    peru = "Peru"
    chile = "Chile"
    argentina = "Argentina"
    uruguay = "Uruguay"
    brasil = "Brasil"
    guyane = "Guyane Fr"
    sunname = "Sunname"
    guyana = "Guyana"
    venezuela = "Venezuela"
    bolivia = "Bolivia"
    paraguay = "Paraguay"


    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [costa_rica,panama,colombia,ecuador,peru,chile,argentina,uruguay, brasil,guyana,guyane,sunname,venezuela,bolivia,paraguay]
    domains = {
        costa_rica: values[:],
        panama: values[:],
        colombia: values[:],
        ecuador: values[:],
        peru: values[:],
        chile: values[:],
        argentina: values[:],
        uruguay: values[:],
        brasil: values[:],
        guyane: values[:],
        sunname: values[:],
        guyana: values[:],
        venezuela: values[:],
        bolivia: values[:],
        paraguay: values[:]
    }

    neighbours = {
        costa_rica: [panama],
        panama: [costa_rica,colombia],
        colombia: [panama,ecuador,peru,brasil,venezuela],
        ecuador: [colombia,peru],
        peru: [ecuador,colombia,brasil,bolivia,chile],
        chile: [peru,bolivia,argentina],
        argentina: [chile,bolivia,paraguay,brasil,uruguay],
        uruguay: [argentina,brasil],
        bolivia: [peru,brasil,paraguay,argentina,chile],
        paraguay: [argentina,bolivia,brasil],
        brasil: [uruguay,paraguay,bolivia,peru,colombia,venezuela,guyana,sunname,guyane],
        guyane: [brasil,sunname],
        sunname: [brasil,guyana,guyane],
        guyana: [sunname,brasil,venezuela],
        venezuela: [colombia,brasil,guyana]
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        costa_rica: constraint_function,
        panama: constraint_function,
        colombia: constraint_function,
        ecuador: constraint_function,
        peru: constraint_function,
        chile: constraint_function,
        argentina: constraint_function,
        uruguay: constraint_function,
        bolivia: constraint_function,
        paraguay: constraint_function,
        brasil: constraint_function,
        guyane: constraint_function,
        sunname: constraint_function,
        guyana: constraint_function,
        venezuela: constraint_function
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    australia = create_sa_csp()
    result = australia.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
