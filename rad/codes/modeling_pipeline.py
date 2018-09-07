from subprocess import run

from paraview.simple import OpenDataFile
import liboofem

PUT_DO_OOFEM_KONVERTERA = '../oofem/tools/unv2oofem/unv2oofem.py'

UNV_DATOTEKA = 'salome_izlazna_datoteka.unv'
KONTROLNA_DATOTEKA = 'kontrolna_datoteka.ctrl'
OOFEM_ULAZ = 'oofem_ulazna_datoteka.in'

# Pretvaranje ulaznih podataka u pogodan oblik
run(['python', PUT_DO_OOFEM_KONVERTERA, UNV_DATOTEKA, KONTROLNA_DATOTEKA, OOFEM_ULAZ])

podaci = liboofem.OOFEMTXTDataReader(OOFEM_ULAZ)

problem = liboofem.InstanciateProblem(podaci, liboofem.problemMode._processor, 0)

'''
Dio koda u kojem se mogu napraviti dodatne izmjene poput dodavanje novih materijala,
rubnih uvjeta, konacnih elemenata i slicno. 
Primjer dodavanja novog elementa
domena = problem.giveDomain(1)
novi_broj_elemenata = domena.giveNumberOfElements() + 1
novi_element = liboofem.element('truss2d', novi_broj_elemenata, domena, nodes=(1, 2))
domena.resizeElements(len(konacni_elementi))
domena.setElement(novi_element.number, novi_broj_elemenata)
'''

# Rjesavanje problema
problem.checkProblemConsistency()
problem.setRenumberFlag()
problem.solveYourself()
problem.terminateAnalysis()

IZLAZNA_DATOTEKA = problem.outputBaseFileName

# Ucitavanje podataka u ParaView koja odraduje vizualizaiju
OpenDataFile(IZLAZNA_DATOTEKA)
