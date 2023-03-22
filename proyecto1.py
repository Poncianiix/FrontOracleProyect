from pymongo import MongoClient
from bson.objectid import ObjectId
import flet
import requests

from flet import (
    Column,
    ElevatedButton,
    alignment,
    TextField,
    AppBar,
    Container,
    FloatingActionButton,
    Icon,
    NavigationRail,
    NavigationRailDestination,
    Page,
    Row,
    Text,
    VerticalDivider,
    View,
    colors,
    icons,
    AlertDialog,
    padding,
    TextButton,
    ListView,
    Card,
    ListTile,
    PopupMenuButton,
    PopupMenuItem,
    Image,
    Dropdown,
    dropdown,
    
)


def main(page: Page):

    listaPrestamos = []
    listaManagers = []

    ## Se crean los textos que se van a mostrar en la pantalla
    ##################################################################################################################################################################

    #idsucursal, nombresucursal, ciudadsucursal, activos, region
    txtIdSuc = TextField(label="Id de sucursal")
    txtNomSuc = TextField(label="Nombre de sucursal")
    txtCdSuc = TextField(label="Ciudad de sucursal")
    txtActi = TextField(label="Activos")
    txtReg = TextField(label="Region")

    #  constructor(noprestamo, idsucursal, cantidad) {
    txtNumPres = TextField(label="Numero de prestamo")
    txtIdSuc2 = TextField(label="Id de sucursal")
    txtCant = TextField(label="Cantidad")

    rail = NavigationRail(
        selected_index=0,
        label_type="all",
        # extended=True,
        min_width=100,
        min_extended_width=400,
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=icons.WAREHOUSE_OUTLINED, selected_icon=icons.WAREHOUSE, label="Sucursales"
            ),
            NavigationRailDestination(
                icon=icons.MONEY_OFF,selected_icon=icons.ATTACH_MONEY,label="Prestamos",
            ),
            NavigationRailDestination(
                icon=icons.LIST,selected_icon=icons.LIST,label="Lista de sucursales",
            ),
            NavigationRailDestination(
                icon=icons.LIST_ALT,selected_icon=icons.LIST_ALT,label="Lista de prestamos",
            ),
            NavigationRailDestination(
                icon=icons.FORMAT_LIST_NUMBERED,selected_icon=icons.FORMAT_LIST_NUMBERED,label="Prestamos por sucursal",
            ),
           
        ],
        #on_change=lambda e: print("Selected destination:", e.control.selected_index),
        on_change=lambda e: goPage(e.control.selected_index),
    )


## Funcion para limpiar los campos de texto

    def limpiarCampos():
        txtIdSuc.value = ""
        txtNomSuc.value = ""
        txtCdSuc.value = ""
        txtActi.value = ""
        txtReg.value = ""
        txtNumPres.value = ""
        txtIdSuc2.value = ""
        txtCant.value = ""

##################################################################################################################################################################


## Funciones para las notificaciones
##################################################################################################################################################################

    def closeOk(e):
        insertOk.open = False
        page.update()

    def closeErr(e):
        insertError.open = False
        page.update()

    def closeDatosNoValidos(e):
        datosNoValidos.open = False
        page.update()

    def closeUpdateEmpOk(e):
        lv.controls.clear()
        global idAuxiliar
        idAuxiliar = " "
        updateOk.open = False
        listarSucursales()
        page.clean()
        page.add(
                Row(
            [
                rail,
                VerticalDivider(width=1),
                Column([  
                Container(content=lv, width=1000,height = 900, padding=padding.only(left=50,top=1,bottom=200)),
                ],spacing=10,),             
            ],
            height=1000,
            
                )
            )
        page.update()

    def closeUpdateEmpErr(e):
        updateError.open = False
        page.update()
    
    def closeDeleteEmpOk(e):
        lv.controls.clear()
        deleteOk.open = False
        listarSucursales()
        page.clean()
        page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        Column([  
                            Container(content=lv, width=1000,height = 900, padding=padding.only(left=50,top=1,bottom=200)),
                        ],spacing=10,),
                    ],
                    height=1000,
            
                )
        )
        page.update()

    def closeDeleteEmpErr(e):
        deleteError.open = False
        page.update()

    def closeDeleteDeptOk(e):
        lvDept.controls.clear()
        deleteOkDept.open = False
        listarPrestamos()
        page.clean()
        page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        Column([  
                            Container(content=lvDept, width=1000,height = 900, padding=padding.only(left=50,top=1,bottom=200)),
                        ],spacing=10,),

             
                    ],
                    height=1000,
            
                )
        )
        page.update()

    def closeDeleteDeptErr(e):
        deleteErrorDept.open = False
        page.update()

    def closeUpdateDeptOk(e):
        lvDept.controls.clear()
        global idAuxiliar
        idAuxiliar = " "
        updateOkDeptn.open = False
        listarPrestamos()
        page.clean()
        page.add(
                Row(
            [
                rail,
                VerticalDivider(width=1),
                Column([  
                Container(content=lvDept, width=1000,height = 900, padding=padding.only(left=50,top=1,bottom=200)),
               
                
                ],spacing=10,),

             
            ],
            height=1000,
            
                )
            )
        page.update()

    def closeUpdateDeptErr(e):
        updateErrorDeptn.open = False
        page.update()
    

    insertOk = AlertDialog(
        modal=True,
        title=Text("Registro creado con exito"),
        actions=[
            TextButton("Ok", on_click=closeOk),
        ],
        actions_alignment="end",
    )

    insertError = AlertDialog(
        modal=True,
        title=Text("Error al registrar"),
        actions=[
            TextButton("OK", on_click=closeErr),
        ],
        actions_alignment="end",
    )

    datosNoValidos = AlertDialog(
        modal=True,
        title=Text("Datos no validos"),
        actions=[
            TextButton("OK", on_click=closeDatosNoValidos),
        ],
        actions_alignment="end",
    )

    updateOk = AlertDialog(
        modal=True,
        title=Text("Actualizacion realizada con exito"),
        actions=[
            TextButton("Ok", on_click=closeUpdateEmpOk),
        ],
        actions_alignment="end",
    )

    updateError = AlertDialog(
        modal=True,
        title=Text("Error al actualizar"),
        actions=[
            TextButton("OK", on_click=closeUpdateEmpErr),
        ],
        actions_alignment="end",
    )

    updateOkDeptn = AlertDialog(
        modal=True,
        title=Text("Actualizacion realizada con exito"),
        actions=[
            TextButton("Ok", on_click=closeUpdateDeptOk),
        ],
        actions_alignment="end",
    )

    updateErrorDeptn  = AlertDialog(
        modal=True,
        title=Text("Error al actualizar"),
        actions=[
            TextButton("OK", on_click=closeUpdateDeptErr),
        ],
        actions_alignment="end",
    )


    deleteOk = AlertDialog(
        modal=True,
        title=Text("Empleado eliminado con exito"),
        actions=[
            TextButton("Ok", on_click=closeDeleteEmpOk),
        ],
        actions_alignment="end",
    )

    deleteError = AlertDialog(
        modal=True,
        title=Text("Error al eliminar el empleado"),
        actions=[
            TextButton("OK", on_click=closeDeleteEmpErr),
        ],
        actions_alignment="end",
    )

    deleteOkDept = AlertDialog(
        modal=True,
        title=Text("Departamento eliminado con exito"),
        actions=[
            TextButton("Ok", on_click=closeDeleteDeptOk),
        ],
        actions_alignment="end",
    )

    deleteErrorDept = AlertDialog(
        modal=True,
        title=Text("Error al eliminar el Departamento"),
        actions=[
            TextButton("OK", on_click=closeDeleteDeptErr),
        ],
        actions_alignment="end",
    )



##################################################################################################################################################################


## Funciones para el CRUD de empleados
##################################################################################################################################################################

    def registarSucursal(sucursal):
        
       
        response = requests.post('http://localhost:3000/sucursales/', json=sucursal)
          # Verificar si la respuesta es exitosa
        if response.status_code == 201:
                # Mostrar un mensaje de éxito
            print('Los datos se han agregado exitosamente.')
            page.dialog = insertOk
            insertOk.open = True
            page.update()
        elif response.status_code == 406:
                # Mostrar un mensaje de error en caso de que ocurra un error en el servidor
            print('Error en los datos ingresados.')
            page.dialog = insertError
            insertError.open = True
            page.update()
        else:
            print('Error en el servidor.')

    def eliminarSucursal(string):
        
        sucID = string.split(" ")
        url = 'http://localhost:3000/sucursales/' 
        url2 = url + sucID[2]
        response = requests.get(url2)
        sucursal = response.json()
        payload = {
          
            'region': sucursal[4]
        }
        print(payload)
        response = requests.delete(url2, json=payload)
             # Verificar si la respuesta es exitosa
        if response.status_code == 201:
                # Mostrar un mensaje de éxito
            print('Los datos se a eliminado exitosamente.')
            page.dialog = deleteOk
            deleteOk.open = True
            page.update()
        elif response.status_code == 406:
                # Mostrar un mensaje de error en caso de que ocurra un error en el servidor
            print('Error en los datos ingresados.')
            page.dialog = deleteError
            deleteError.open = True
            page.update()
        else:
            print('Error en el servidor.')
    
    def editarSucursal(sucursal,idSuc):

        url = 'http://localhost:3000/sucursales/' 
        url2 = url + idSuc
        response = requests.put(url2, json=sucursal)

          # Verificar si la respuesta es exitosa
        if response.status_code == 201:
                # Mostrar un mensaje de éxito
            print('Los datos se han modificado exitosamente.')
            page.dialog = updateOk
            updateOk.open = True
            page.update()
        elif response.status_code == 406:
                # Mostrar un mensaje de error en caso de que ocurra un error en el servidor
            print('Error en los datos ingresados.')
            page.dialog = updateError
            updateError.open = True
            page.update()
        else:
            print('Error en el servidor.')

    def llenarSucursal(string):
        
        sucID = string.split(" ")
        url = 'http://localhost:3000/sucursales/' 
        url2 = url + sucID[2]
        response = requests.get(url2)
        sucursales = response.json()
        try:
            
            txtIdSuc.value = sucursales[0]
            txtNomSuc.value = sucursales[1]
            txtCdSuc.value = sucursales[2]
            txtActi.value = sucursales[3]
            txtReg.value = sucursales[4]
            
            page.clean()
            page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        Column([  
                        Container(width=1000,height=30,padding=padding.only(left=50,top=1)),
                        Container(content=txtNomSuc, width=1000,height=80,padding=padding.only(left=50,top=1)),
                        Container(content=txtCdSuc, width=1000,height=80,padding=padding.only(left=50,top=1)),
                        Container(content=txtActi, width=1000,height=80,padding=padding.only(left=50,top=1)),
                       
                        ElevatedButton("Modificar Sucursal", on_click=botonActualizarSucursal)
                
                        ],spacing=10,),

             
                    ],
                    height=1000,
                )
            )
            page.update()

        except Exception as e:
            print(e)

    def botonSucursal(e):
        if not txtIdSuc.value:
            txtIdSuc.error_text = "Por favor ingrese el id de la sucursal"
            page.update()
        elif not txtNomSuc.value:
            txtNomSuc.error_text = "Por favor ingrese el nombre de la sucursal"
            page.update()
        elif not txtCdSuc.value:
            txtCdSuc.error_text = "Por favor ingrese la ciudad de la sucursal"
            page.update()
        elif not txtActi.value:
            txtActi.error_text = "Por favor ingrese el activo de la sucursal"
            page.update()
        elif not txtReg.value:
            txtReg.error_text = "Por favor ingrese la region de la sucursal"
            page.update()
        else:
             #idsucursal, nombresucursal, ciudadsucursal, activos, region
            try:
                sucursal = {
                "idsucursal": txtIdSuc.value,
                "nombresucursal": txtNomSuc.value,
                "ciudadsucursal": txtCdSuc.value,
                "activos": int(txtActi.value),
                "region": int(txtReg.value)
                }
                registarSucursal(sucursal)
                limpiarCampos()
                page.update()
            except Exception as e:
                print(e)
                page.dialog = datosNoValidos
                datosNoValidos.open = True
                page.update()
            
    def botonActualizarSucursal(e):

        if not txtIdSuc.value:
            txtIdSuc.error_text = "Por favor ingrese el id de la sucursal"
            page.update()
        elif not txtNomSuc.value:
            txtNomSuc.error_text = "Por favor ingrese el nombre de la sucursal"
            page.update()
        elif not txtCdSuc.value:
            txtCdSuc.error_text = "Por favor ingrese la ciudad de la sucursal"
            page.update()
        elif not txtActi.value:
            txtActi.error_text = "Por favor ingrese el activo de la sucursal"
            page.update()
        elif not txtReg.value:
            txtReg.error_text = "Por favor ingrese la region de la sucursal"
            page.update()
        else:
             #idsucursal, nombresucursal, ciudadsucursal, activos, region
            try:
                sucursal = {
                "idsucursal": txtIdSuc.value,
                "nombresucursal": txtNomSuc.value,
                "ciudadsucursal": txtCdSuc.value,
                "activos": int(txtActi.value),
                "region": int(txtReg.value)
                }
                editarSucursal(sucursal,txtIdSuc.value)
                limpiarCampos()
                page.update()
            except Exception as e:
                print(e)
                page.dialog = datosNoValidos
                datosNoValidos.open = True
                page.update()        

##################################################################################################################################################################

     
## Funciones para el CRUD de departamentos
##################################################################################################################################################################

    def registrarPrestamo(prestamo):
      
        response = requests.post('http://localhost:3000/prestamos/', json=prestamo)
          # Verificar si la respuesta es exitosa
        if response.status_code == 201:
                # Mostrar un mensaje de éxito
            print('Los datos se han agregado exitosamente.')
            page.dialog = insertOk
            insertOk.open = True
            page.update()
        elif response.status_code == 406:
                # Mostrar un mensaje de error en caso de que ocurra un error en el servidor
            print('Error en los datos ingresados.')
            page.dialog = insertError
            insertError.open = True
            page.update()
        else:
            print('Error en el servidor.')
            
    def eliminarPrestamo(string):
        
        sucID = string.split(" ")
        url = 'http://localhost:3000/prestamos/' 
        url2 = url + sucID[2]
        response = requests.get(url2)
        prestamo = response.json()
        payload = {
            "noprestamo": prestamo[0],
            "idsucursal": prestamo[1],
            "cantidad": prestamo[2]
        }
        response = requests.delete(url2, json=payload)
             # Verificar si la respuesta es exitosa
        if response.status_code == 201:
                # Mostrar un mensaje de éxito
            print('Los datos se a eliminado exitosamente.')
            page.dialog = deleteOkDept
            deleteOkDept.open = True
            page.update()
        elif response.status_code == 406:
                # Mostrar un mensaje de error en caso de que ocurra un error en el servidor
            print('Error en los datos ingresados.')
            page.dialog = deleteError
            deleteError.open = True
            page.update()
        else:
            print('Error en el servidor.')

    def editarPrestamo(prestamo,idSuc):
        
        url = 'http://localhost:3000/prestamos/' 
        url2 = url + idSuc
        response = requests.put(url2, json=prestamo)

          # Verificar si la respuesta es exitosa
        if response.status_code == 201:
                # Mostrar un mensaje de éxito
            print('Los datos se han modificado exitosamente.')
            page.dialog = updateOkDeptn
            updateOkDeptn.open = True
            page.update()
        elif response.status_code == 406:
                # Mostrar un mensaje de error en caso de que ocurra un error en el servidor
            print('Error en los datos ingresados.')
            page.dialog = updateErrorDeptn
            updateErrorDeptn.open = True
            page.update()
        else:
            print('Error en el servidor.')

    def llenarPrestamo(string):
                        #  constructor(noprestamo, idsucursal, cantidad) {

        sucID = string.split(" ")
        url = 'http://localhost:3000/prestamos/' 
        url2 = url + sucID[2]
        response = requests.get(url2)
        prestamos = response.json()
        print(prestamos)
        try:
            txtNumPres.value = prestamos[0]
            txtIdSuc2.value = prestamos[1]
            txtCant.value = prestamos[2]
            
            page.clean()
            page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        Column([  
                            Container(width=1000,height=30,padding=padding.only(left=50,top=1)),
                            Container(content=txtCant, width=1000,height=80,padding=padding.only(left=50,top=1)),
                            ElevatedButton("Modificar Prestamo", on_click=botonActualizarPrestamo),
                
                       
                        ],spacing=10,),

             
                    ],
                    height=1000,
                )
            )
            page.update()

        except Exception as e:
            print(e)

    def botonPrestamo(e):
        if not txtNumPres.value:
            txtNumPres.error_text = "Por favor ingrese el numero de prestamo"
            page.update()
        elif not txtIdSuc2.value:
            txtIdSuc2.error_text = "Por favor ingrese el id de la sucursal"
            page.update()
        elif not txtCant.value:
            txtCant.error_text = "Por favor ingrese la cantidad"
            page.update()
        else:            
            try:
                prestamo = {
                "noprestamo": txtNumPres.value,
                "idsucursal": txtIdSuc2.value,
                "cantidad": int(txtCant.value)
                }
                registrarPrestamo(prestamo)
                limpiarCampos()
                page.update()
            except Exception as e:
                print(e)
                page.dialog = datosNoValidos
                datosNoValidos.open = True
                page.update()

    def botonActualizarPrestamo(e):
        if not txtNumPres.value:
            txtNumPres.error_text = "Por favor ingrese el numero de prestamo"
            page.update()
        elif not txtIdSuc2.value:
            txtIdSuc2.error_text = "Por favor ingrese el id de la sucursal"
            page.update()
        elif not txtCant.value:
            txtCant.error_text = "Por favor ingrese la cantidad"
            page.update()
        else:            
            try:
                prestamo = {
                "noprestamo": txtNumPres.value,
                "idsucursal": txtIdSuc2.value,
                "cantidad": int(txtCant.value)
                }
                editarPrestamo(prestamo,txtNumPres.value)
                limpiarCampos()
                page.update()
            except Exception as e:
                print(e)
                page.dialog = datosNoValidos
                datosNoValidos.open = True
                page.update()

##################################################################################################################################################################
    

##################################################################################################################################################################    

## Inicializacion de la aplicacion
    #page.scroll = "always"    
    page.add(
        Row(
            [
                rail,
                VerticalDivider(width=1),
                Column([  
                Container(width=1000,height=30,padding=padding.only(left=50,top=1)),
                Container(content=txtIdSuc, width=1000,height=80,padding=padding.only(left=50,top=1)),
                Container(content=txtNomSuc, width=1000,height=80,padding=padding.only(left=50,top=1)),
                Container(content=txtCdSuc, width=1000,height=80,padding=padding.only(left=50,top=1)),
                Container(content=txtActi, width=1000,height=80,padding=padding.only(left=50,top=1)),
                Container(content=txtReg, width=1000,height=80,padding=padding.only(left=50,top=1)),
   
                
                ElevatedButton("Registrar Sucursal", on_click=botonSucursal)
                
                ],spacing=10,),

             
            ],
            height=1000,
        )
    )
##################################################################################################################################################################

## Funcion para cargar los datos en la tabla
    lv = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    lvDept = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    def listarSucursales():
        response = requests.get('http://localhost:3000/sucursales/')
        sucursales = response.json()
        for i in range(0, len(sucursales)):
            lv.controls.append(
                ListTile(
                            leading=Icon(icons.WAREHOUSE),
                            
                            title=Text("Sucursal: " + sucursales[i][1] + " - " + sucursales[i][2] + " - "+ " Region: " + str(sucursales[i][4])),
                            subtitle=Text("Cantidad de activos: " + "$" +str(sucursales[i][3])),
                   
                            trailing=PopupMenuButton(
                                icon=icons.MORE_VERT,
                                items=[
                                    PopupMenuItem(text="Borrar a " + str(sucursales[i][0]),on_click=lambda e: eliminarSucursal(e.control.text)),
                                    PopupMenuItem(text="Editar a " + str(sucursales[i][0]),on_click=lambda e: llenarSucursal(e.control.text)),
                                ],
                            ),
                            #on_click= eliminarSucursal(empleados[i]["_id"]),
                        ),
            )
    
    def listarPrestamos():
        response = requests.get('http://localhost:3000/prestamos/')
        prestamos = response.json()
        for i in range(0, len(prestamos)):
            lvDept.controls.append(
                ListTile(
                            leading=Icon(icons.ATTACH_MONEY),
                            title=Text("Prestamos No: " + prestamos[i][0] + " Pertenece a la sucursal: " + prestamos[i][1]),
                            subtitle=Text("Cantidad de prestamo: " + "$" + str(prestamos[i][2])),
                          
                            trailing=PopupMenuButton(
                                icon=icons.MORE_VERT,
                                items=[
                                    PopupMenuItem(text="Borrar a " + str(prestamos[i][0]),on_click=lambda e: eliminarPrestamo(e.control.text)),
                                    PopupMenuItem(text="Editar a " + str(prestamos[i][0]),on_click=lambda e: llenarPrestamo(e.control.text)),

                                ],
                            ),
                            #on_click= eliminarSucursal(empleados[i]["_id"]),
                        ),
            )
    def listarPrestamosPorSucursal():
        response = requests.get('http://localhost:3000/prestamos/sucursal/sucursal')
        prestamos = response.json()
        print(prestamos)
        for i in range(0, len(prestamos)):
            lvDept.controls.append(
                ListTile(
                            leading=Icon(icons.ATTACH_MONEY),
                            title=Text("Sucursal No: " + prestamos[i][0]),
                            subtitle=Text("Total del prestamo: " + "$" + str(prestamos[i][1])),
                            #on_click= eliminarSucursal(empleados[i]["_id"]),
                        ),
            )
            

##################################################################################################################################################################

## Funciones para las rutas de la aplicación      
##################################################################################################################################################################
    
    def goPage(index):
      
        if(index == 0):
            page.route = "/registroSucursal"
            limpiarCampos()
            page.update()
        elif(index == 1):
            page.route = "/registroPrestamo"
            limpiarCampos()
            page.update()
        elif(index == 2):
            lvDept.controls.clear()
            lv.controls.clear()
            listarSucursales()
            page.route = "/listaSucursales"
            limpiarCampos()
            page.update()
        elif(index == 3):
            lvDept.controls.clear()
            lv.controls.clear()
            listarPrestamos()
            page.route = "/listaPrestamos"
            limpiarCampos()
            page.update()
        elif(index == 4):
            lvDept.controls.clear()
            lv.controls.clear()
            listarPrestamosPorSucursal()
            page.route = "/listaPrestamos"
            limpiarCampos()
            page.update()

    def routeChange(route):
        print(page.route)
        if(page.route == "/registroSucursal"):
            page.clean()
            page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        
                        Column([  
                            Container(width=1000,height=30,padding=padding.only(left=50,top=1)),
                            Container(content=txtIdSuc, width=1000,height=80,padding=padding.only(left=50,top=1)),
                            Container(content=txtNomSuc, width=1000,height=80,padding=padding.only(left=50,top=1)),
                            Container(content=txtCdSuc, width=1000,height=80,padding=padding.only(left=50,top=1)),
                            Container(content=txtActi, width=1000,height=80,padding=padding.only(left=50,top=1)),
                            Container(content=txtReg, width=1000,height=80,padding=padding.only(left=50,top=1)),
   
                
                            ElevatedButton("Registrar Sucursal", on_click=botonSucursal)
                
                        ],spacing=10,),

             
                    ],
                    height=1000,
                )
            )
            page.update()
        if(page.route == "/registroPrestamo"):
            page.clean()
            page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        Column([
                            Container(width=1000,height=30,padding=padding.only(left=50,top=1)),
                            Container(content=txtNumPres, width=1000,height=80,padding=padding.only(left=50,top=1)),
                            Container(content=txtIdSuc2, width=1000,height=80,padding=padding.only(left=50,top=1)),
                            Container(content=txtCant, width=1000,height=80,padding=padding.only(left=50,top=1)),
                            ElevatedButton("Registrar Prestamo", on_click=botonPrestamo)
                        ],spacing=10,),
                    ],
                    height=1000,
                )
            )
            page.update()
        if(page.route == "/listaSucursales"):
 
            page.clean()
            page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        Column([  
                            Container(content=lv, width=1000,height = 900, padding=padding.only(left=50,top=1,bottom=200)),
                        ],spacing=10,),

                    ],
                    height=1000,
                )
            )
        if(page.route == "/listaPrestamos"):
 
            page.clean()
            page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        Column([  
                            Container(content=lvDept, width=1000,height = 900, padding=padding.only(left=50,top=1,bottom=200)),
                        ],spacing=10,),

                    ],
                    height=1000,
                )
            )
        if(page.route == "/listaPrestamosPorSucursal"):
 
            page.clean()
            page.add(
                Row(
                    [
                        rail,
                        VerticalDivider(width=1),
                        Column([  
                            Container(content=lvDept, width=1000,height = 900, padding=padding.only(left=50,top=1,bottom=200)),
                        ],spacing=10,),

                    ],
                    height=1000,
                )
            )
            page.update()

##################################################################################################################################################################
    
    page.on_route_change = routeChange

flet.app(target=main)

