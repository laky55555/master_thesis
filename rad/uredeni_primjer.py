import liboofem

# Definicija analize koja ce se provesti
problem = liboofem.linearStatic(nSteps=3, outFile="izlazni_podaci2.out")

# Domena i izlazni podaci koji ce se sacuvati
domena = liboofem.domain(1, 1, problem, liboofem.domainType._2dBeamMode, tstep_all=True,
                         dofman_all=True, element_all=True)
problem.setDomain(1, domena, True)

# Za svaki objekt koji nasljeduje klasu FEMComponent ukoliko priliko inicijalizacije
# nema definiranu domenu pridruzuje se zadnjoj inicijaliziranoj

# Slicno kao i gore, ako nije odreden broj komponente dodjeljuje mu se iduci po redu
# npr. za peakFunction dodjeljuje joj se domain.numberOfLoadTimeFunctions + 1
# Analogno i za sve ostale klase nasljednice FEMComponent klase

vremenska_funk_1 = liboofem.peakFunction(1, domena, t=1, f_t=1)
vremenska_funk_2 = liboofem.peakFunction(2, domena, t=2, f_t=1)
vremenska_funk_3 = liboofem.peakFunction(3, domena, t=3, f_t=1)
vremenske_funkcije = (vremenska_funk_1, vremenska_funk_2, vremenska_funk_3)

# loadTimeFunction parametar moze se zadati putem broja ili direktno (vidi primjere)
# Analogno vrijedi i za sve ostale objekte koji implementiraju metodu giveNumber()

# Ukoliko se od nekog parametra ocekuje niz, zadaje se pomocu liste i n-torke

# Rubni uvjeti
rubni_uvjet_1 = liboofem.boundaryCondition(1, domena, loadTimeFunction=1,
                                           prescribedValue=0.0)
rubni_uvjet_2 = liboofem.boundaryCondition(2, domena, loadTimeFunction=2,
                                           prescribedValue=-.006e-3)

opterecenje_po_rubu = liboofem.constantEdgeLoad(3, domena, loadTimeFunction=1,
                                                components=(0., 10., 0.), loadType=3,
                                                ndofs=3)

opterecenje_u_cvoru = liboofem.nodalLoad(4, domena, loadTimeFunction=1,
                                         components=(-18., 24., 0.))

opterecenje_temper = liboofem.structTemperatureLoad(5, domena,
                                                    loadTimeFunction=vremenska_funk_3,
                                                    components=(30., -20.))
uvjeti_i_opterecenja = (
    rubni_uvjet_1, rubni_uvjet_2, opterecenje_po_rubu, opterecenje_u_cvoru,
    opterecenje_temper)

# Cvorovi
cvor_1 = liboofem.node(1, domena, coords=(0., 0., 0.), bc=(0, 1, 0))
cvor_2 = liboofem.node(2, domena, coords=(2.4, 0., 0.), bc=(0, 0, 0))
cvor_3 = liboofem.node(3, domena, coords=(3.8, 0., 0.), bc=(0, 0, rubni_uvjet_1))
cvor_4 = liboofem.node(4, domena, coords=(5.8, 0., 1.5), bc=(0, 0, 0), load=(4,))
cvor_5 = liboofem.node(5, domena, coords=(7.8, 0., 3.0), bc=(0, 1, 0))
cvor_6 = liboofem.node(6, domena, coords=(2.4, 0., 3.0),
                       bc=(rubni_uvjet_1, 1, rubni_uvjet_2))
cvorovi = (cvor_1, cvor_2, cvor_3, cvor_4, cvor_5, cvor_6)

# Materijali i poprecni presjeci
materijal = liboofem.isoLE(1, domena, d=1., E=30.e6, n=0.2, tAlpha=1.2e-5)
poprecni_presjek = liboofem.simpleCS(1, domena, area=0.162, Iy=0.0039366,
                                     beamShearCoeff=1.e18, thick=0.54)

# Konacni elementi
greda_1 = liboofem.beam2d(1, domena, nodes=(1, cvor_2), mat=1, crossSect=1,
                          boundaryLoads=(3, 1), bodyLoads=(5,))
greda_2 = liboofem.beam2d(2, domena, nodes=(2, 3), mat=materijal, crossSect=1,
                          DofsToCondense=(6,), bodyLoads=[opterecenje_temper])
greda_3 = liboofem.beam2d(3, domena, nodes=(cvor_3, 4), mat=1,
                          crossSect=poprecni_presjek, dofstocondense=[3])
greda_4 = liboofem.beam2d(4, domena, nodes=(cvor_4, cvor_5), mat=materijal,
                          crossSect=poprecni_presjek)
greda_5 = liboofem.beam2d(5, domena, nodes=(cvor_6, 2), mat=1, crossSect=1,
                          DofsToCondense=(6,))
konacni_elementi = (greda_1, greda_2, greda_3, greda_4, greda_5)

# Potrebno je sad popuniti domenu s novoinicijaliziranim komponentama

# Radi dobivanja na brzini koristi se resize tako da ne dolazi do dinamicne
# realokacije prilikom dodavanja svake nove komponenete

domena.resizeDofManagers(len(cvorovi))
for cvor in cvorovi:
    domena.setDofManager(cvor.number, cvor)

domena.resizeElements(len(konacni_elementi))
for konacni_element in konacni_elementi:
    domena.setElement(konacni_element.number, konacni_element)

domena.resizeMaterials(1)
domena.setMaterial(1, materijal)

domena.resizeCrossSectionModels(1)
domena.setCrossSection(1, poprecni_presjek)

domena.resizeBoundaryConditions(len(uvjeti_i_opterecenja))
for uvjet_opterecenje in uvjeti_i_opterecenja:
    domena.setBoundaryCondition(uvjet_opterecenje.number, uvjet_opterecenje)

domena.resizeFunctions(len(vremenske_funkcije))
for vremenska_funkcija in vremenske_funkcije:
    domena.setFunction(vremenska_funkcija.number, vremenska_funkcija)

problem.checkProblemConsistency()
problem.init()
problem.postInitialize()
problem.setRenumberFlag()
problem.solveYourself()
problem.terminateAnalysis()
