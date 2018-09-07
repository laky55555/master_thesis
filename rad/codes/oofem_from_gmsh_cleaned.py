import liboofem
import pygmsh


def kreiraj_mrezu(datoteka_s_cad_modelom):
    geom = pygmsh.built_in.Geometry()

    with open(datoteka_s_cad_modelom, 'r') as myfile:
        for line in myfile:
            geom.add_raw_code(line)

    geom.add_raw_code('Mesh.Algorithm=8;')

    points, cells, point_data, cell_data, field_data = pygmsh.generate_mesh(geom)

    return points, cells


def kreiraj_vremenske_funkcije(domena):
    vremenska_funkcija = liboofem.loadTimeFunction('ConstantFunction', 1, domena, f_t=1)
    domena.resizeFunctions(1)
    domena.setFunction(vremenska_funkcija.number, vremenska_funkcija)


def kreiraj_cvorove(gmsh_cvorovi, domena):
    domena.resizeDofManagers(len(gmsh_cvorovi))
    for indeks, koordinate in enumerate(gmsh_cvorovi, 1):
        domena.setDofManager(indeks,
                             liboofem.node(indeks, domena, coords=tuple(koordinate)))


def kreiraj_materijale_i_presjeke(domena):
    poprecni_presjek = liboofem.simpleCS(1, domena, area=1, thick=1)
    domena.resizeCrossSectionModels(1)
    domena.setCrossSection(1, poprecni_presjek)

    materijal = liboofem.isoLE(1, domena, d=1., E=200.e4, n=0.2, tAlpha=1.2e-5)
    domena.resizeMaterials(1)
    domena.setMaterial(1, materijal)


def kreiraj_konacne_elemente(gmsh_elementi, domena):
    # Za trokutaste elemente koristimo tr_shell01. Ljuske koje kombiniraju CCT3D element
    # (Mindlinova hipoteza) s trokutastim elementom opterecenja i 6 stupnjeva slobode.
    domena.resizeElements(len(gmsh_elementi['triangle']) + len(gmsh_elementi['quad']))
    for indeks, trokut in enumerate(gmsh_elementi['triangle'] + 1, 1):
        domena.setElement(indeks, liboofem.element('tr_shell01', indeks, domena,
                                                   nodes=tuple(trokut), mat=1,
                                                   crossSect=1, nip=4))

    last_indeks = indeks
    # Za cetverokutne elemente koristimo mitc4shell koji su bilinearni elementi
    # sastavljeni od cetiri cvora po uzoru na MITC tehniku.
    for indeks, cetverokut in enumerate(gmsh_elementi['quad'] + 1, last_indeks + 1):
        domena.setElement(indeks, liboofem.element('quad1mindlin', indeks, domena,
                                                   nodes=tuple(cetverokut), mat=1,
                                                   crossSect=1))


def kreiraj_opterecenja(domena):
    pass


def inicijaliziraj_ulazne_podatke(gmsh_cvorovi, gmsh_elementi, datoteka_izlaza):
    problem = liboofem.linearStatic(nSteps=1, outFile=datoteka_izlaza)

    domena = liboofem.domain(1, 1, problem, liboofem.domainType._3dShellMode,
                             tstep_all=True, dofman_all=True, element_all=True)
    problem.setDomain(1, domena, True)

    kreiraj_cvorove(gmsh_cvorovi, domena)
    kreiraj_konacne_elemente(gmsh_elementi, domena)
    kreiraj_materijale_i_presjeke(domena)
    kreiraj_opterecenja(domena)
    kreiraj_vremenske_funkcije(domena)

    return problem


def napravi_analizu(problem):
    problem.checkProblemConsistency()
    problem.init()
    problem.postInitialize()
    problem.setRenumberFlag()
    problem.solveYourself()
    problem.terminateAnalysis()


gmsh_cvorovi, gmsh_element = kreiraj_mrezu('gmsh_model.txt')
problem = inicijaliziraj_ulazne_podatke(gmsh_cvorovi, gmsh_element, 'rjesenje.out')
napravi_analizu(problem)
