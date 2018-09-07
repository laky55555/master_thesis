import liboofem

podaci = liboofem.OOFEMTXTDataReader("zadatak_terminal.in")

problem = liboofem.InstanciateProblem(podaci, liboofem.problemMode._processor, 0)

problem.checkProblemConsistency()
problem.setRenumberFlag()
problem.solveYourself()
problem.terminateAnalysis()

problem.printYourself()
'''
EngineeringModel: instance StaticStructural
number of steps: 1
number of eq's : 3
'''
print(problem.outputBaseFileName)  # rezultat.out

vremenski_korak = problem.giveCurrentStep()
print(vremenski_korak.giveTimeIncrement())  # 1.0
print(vremenski_korak.giveIntrinsicTime())  # 1.0
print(vremenski_korak.giveTargetTime())  # 1.0

# Prvo dohvatimo domenu koja ce nam sluziti kao izvor podataka
domena = problem.giveDomain(1)

# Dohvatimo prvi cvor
node = domena.giveDofManager(1)
node.printYourself()
'''
Node 1    coord : x 0.000000  y 0.000000  z 0.000000
dof 1  of Node 1 :
equation -1    bc 1 
dof 3  of Node 1 :
equation -2    bc 1 
load array : IntArray of size : 0
'''

# Dohvatimo prvi element domene
element = domena.giveElement(1)
print(element.giveClassName())  # Truss2d
print(element.computeLength())  # 2.5
print(element.giveNumberOfDofManagers())  # 2
print(element.giveDofManager(1).coordinates.printYourself())  # FloatArray (0, 0, 0)
print(element.giveDofManager(1).coordinates.printYourself())  # FloatArray (2.5, 0, 0)
print(element.geometryType)  # liboofem.Element_Geometry_Type.EGT_line_1

integration_rule = element.defaultIntegrationRule
print(integration_rule.giveNumberOfIntegrationPoints())  # 1

integration_point = integration_rule.getIntegrationPoint(0)
print(integration_point)  # <liboofem.GaussPoint object at 0x7f6be5ace910>

'''
Izvorna biblioteka liboofem ne implementira CharType klasu stoga bez modifikacije
nemoguce je koristiti metode na konacnim elementima poput
giveCharacteristicMatrix, giveCharacteristicValue i element.giveCharacteristicVector
jer je potpis tih funkcija na primjeru za dohvacanje matrice:
giveCharacteristicMatrix(oofem::PyElement {lvalue}, oofem::FloatMatrix {lvalue}, 
                         oofem::CharType, oofem::TimeStep*)
'''
# trazena_matrica = liboofem.CharType(1)  # kod matrice krutosti je 1, vise u chartype.h
# matrica_krutosti = liboofem.FloatMatrix()
# matrica_krutosti.resize(4, 4)
# element.giveCharacteristicMatrix(matrica_krutosti, trazena_matrica, vremenski_korak)

poprecni_presjek = element.giveCrossSection()
poprecni_presjek.printYourself()
'''
Cross Section with properties : 
Dictionary : 
   Pair (403,1.000000)
   Pair (404,0.000000)
   Pair (405,0.000000)
   Pair (406,0.000000)
   Pair (402,0.000000)
   Pair (407,0.000000)
   Pair (408,0.000000)
   Pair (409,0.000000)
   Pair (410,0.000000)
   Pair (411,0.000000)
'''

print(domena.giveNumberOfBoundaryConditions())  # 4
rubni_uvjet = domena.giveBc(1)
print(rubni_uvjet.isImposed(vremenski_korak))  # True
