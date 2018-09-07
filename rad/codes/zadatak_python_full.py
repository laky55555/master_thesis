import liboofem

problem = liboofem.linearStatic(nSteps=1, outFile="rezultat_python_full.out")

domena = liboofem.domain(1, 1, problem, liboofem.domainType._2dTrussMode, tstep_all=True,
                         dofman_all=True, element_all=True)
problem.setDomain(1, domena, True)

vremenska_funkcija = liboofem.loadTimeFunction('ConstantFunction', 1, domena, f_t=1)
domena.resizeFunctions(1)
domena.setFunction(vremenska_funkcija.number, vremenska_funkcija)

rubni_uvjet_1 = liboofem.boundaryCondition(1, domena, loadTimeFunction=1,
                                           prescribedValue=0.0)
opterecenje_u_cvoru_1 = liboofem.nodalLoad(2, domena, loadTimeFunction=1,
                                           components=(15000., 0.))
opterecenje_u_cvoru_2 = liboofem.nodalLoad(3, domena, loadTimeFunction=1,
                                           components=(0., 5000.))
uvjeti_i_opterecenja = (rubni_uvjet_1, opterecenje_u_cvoru_1, opterecenje_u_cvoru_2)
domena.resizeBoundaryConditions(len(uvjeti_i_opterecenja))
for uvjet_opterecenje in uvjeti_i_opterecenja:
    domena.setBoundaryCondition(uvjet_opterecenje.number, uvjet_opterecenje)

cvor_1 = liboofem.node(1, domena, coords=(0., 0., 0.), bc=(1, 1))
cvor_2 = liboofem.node(2, domena, coords=(2.5, 0., 0.), bc=(0, 1), load=(2,))
cvor_3 = liboofem.node(3, domena, coords=(0., 0., 1.44), bc=(0, 0), load=(3,))
cvorovi = (cvor_1, cvor_2, cvor_3)
domena.resizeDofManagers(len(cvorovi))
for cvor in cvorovi:
    domena.setDofManager(cvor.number, cvor)

materijal = liboofem.isoLE(1, domena, d=1., E=200.e4, n=0.2, tAlpha=1.2e-5)
domena.resizeMaterials(1)
domena.setMaterial(1, materijal)

poprecni_presjek = liboofem.simpleCS(1, domena, area=1)
domena.resizeCrossSectionModels(1)
domena.setCrossSection(1, poprecni_presjek)

greda_1 = liboofem.element('truss2d', 1, domena, nodes=(1, 2), mat=1, crossSect=1)
greda_2 = liboofem.element('truss2d', 2, domena, nodes=(1, 3), mat=1, crossSect=1)
greda_3 = liboofem.element('truss2d', 3, domena, nodes=(2, 3), mat=1, crossSect=1)
konacni_elementi = (greda_1, greda_2, greda_3)
domena.resizeElements(len(konacni_elementi))
for konacni_element in konacni_elementi:
    domena.setElement(konacni_element.number, konacni_element)

problem.checkProblemConsistency()
problem.init()
problem.postInitialize()
problem.setRenumberFlag()
problem.solveYourself()
problem.terminateAnalysis()

