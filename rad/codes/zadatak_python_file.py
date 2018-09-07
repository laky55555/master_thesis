import liboofem

podaci = liboofem.OOFEMTXTDataReader("zadatak_terminal.in")

problem = liboofem.InstanciateProblem(podaci, liboofem.problemMode._processor, 0)

problem.checkProblemConsistency()
problem.setRenumberFlag()
problem.solveYourself()
problem.terminateAnalysis()
