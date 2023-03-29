import React, {useState, useEffect} from 'react'
import axios from "axios";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import swal from 'sweetalert2';
const TablaSucursales = () => {
    const [agrega, setAgrega] = useState(false)
    const [sucursales, setSucursales] = useState([]);
    useEffect(() => {
        if (!agrega)
            obtenerdatos();
    }, [agrega])
    
    const obtenerdatos = async() => {
        const config = {
            method: 'GET',
            url: 'http://localhost:4000/sucursales',
            headers: {
              'Content-Type': 'application/json'
            }
        };

        const response = await axios(config);
        //console.log(response.data);
        setSucursales(response.data);
    }


    const validationSchema = Yup.object().shape({
        idSucursal: Yup.number('Debe ser un numero').required('El ID es obligatorio'),
        nombre: Yup.string().required('El nombre es obligatorio'),
        ciudad: Yup.string().required('la ciudad es obligatoria'),
        region: Yup.number('Debe ser un numero').required('La region es obligatoria'),
        activos: Yup.number('Debe ser un numero').required('Los activos son obligatorios')
    });

    const initialValues = {
        idsucursal: '',
        nombre: '',
        ciudad: '',
        region: '',
        archivos: ''
    }

    const handleSubmit = async(values, { resetForm }) => {
        try {
            const config = {
                method: 'POST',
                url: 'http://localhost:4000/sucursales',
                data: {
                  idsucursal: values.idSucursal,
                  nombresucursal: values.nombre,
                  ciudadsucursal: values.ciudad,
                  activos: values.activos,
                  region: values.region
                },
                headers: {
                  'Content-Type': 'application/json'
                }
              };   
              const response = await axios(config);
              setAgrega(false);
        } catch (error) {
        console.log(error);
        }
        resetForm();
    };

    const deleteSuc = async(suc) => {
        swal.fire({
            title: '¿Estás seguro de que deseas eliminar esta sucursal?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Eliminar',
            cancelButtonText: 'Cancelar'
        }).then(async(result) => {
            if (result.isConfirmed) {
                try {
                    const config = {
                        method: 'DELETE',
                        url: `http://localhost:4000/sucursales/${suc[0]}`,
                        data: {
                            idsucursal: suc[0],
                            nombresucursal: suc[1],
                            ciudadsucursal: suc[2],
                            activos: suc[3],
                            region: suc[4]
                        },
                        headers: {
                        'Content-Type': 'application/json'
                        }
                    };

                    const response = await axios(config);
                    setAgrega(true);
                    setAgrega(false);
                    swal.fire(
                        '¡Eliminado!',
                        'La sucursal ha sido eliminada.',
                        'success'
                    );
                } catch (error) {
                    console.log(error);
                }
                
            }
        });
        
    }

    const editaSuc = (suc) => {
        swal.fire({
            title: 'Ingrese los datos de la sucursal',
            html:
              '<label for="nombre">Nombre:</label>' +
              `<input id="nombre" class="swal2-input" value="${suc[1]}" placeholder="Nombre de la sucursal">` +
              '<label for="ciudad">Ciudad:</label>' +
              `<input id="ciudad" class="swal2-input" value="${suc[2]}" placeholder="Nombre de la ciudad">` +
              '<label for="activos">Activos:</label>' +
              `<input id="activos" type="number" value="${suc[3]}" class="swal2-input" placeholder="Número de activos">`,
            focusConfirm: false,
            preConfirm: () => {
              return {
                nombre: document.getElementById('nombre').value,
                ciudad: document.getElementById('ciudad').value,
                activos: document.getElementById('activos').value
              }
            }
          }).then(async(result) => {
            // Aquí puedes usar los valores ingresados en los inputs
            console.log(result.value);
            try {
                const config = {
                    method: 'PUT',
                    url: `http://localhost:4000/sucursales/${suc[0]}`,
                    data: {
                        idsucursal: suc[0],
                        nombresucursal: result.value.nombre,
                        ciudadsucursal: result.value.ciudad,
                        activos: result.value.activos,
                        region: suc[4]
                    },
                    headers: {
                    'Content-Type': 'application/json'
                    }
                };

                const response = await axios(config);
                setAgrega(true);
                setAgrega(false);
                swal.fire(
                    'Actualizada!',
                    'La sucursal ha sido actualizada.',
                    'success'
                );
            } catch (error) {
                console.log(error);
            }
          });
    }

    return(
        <div className='p-5 font-white'>
            {
                !agrega ? (
                    <div className='flex justify-end mb-2'>
                        <button onClick={() => setAgrega(true)} className='text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800'>Agregar Sucursal</button>
                    </div>
                ) : (
                    <div className='flex justify-start mb-5'>
                        <button onClick={() => setAgrega(false)} className='text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800'>&lt; Regresar</button>
                    </div>
                )
            }
            {
                !agrega ? (
                    <div className="relative overflow-x-auto">
                <table className="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th scope="col" className="px-6 py-3">
                                Nombre
                            </th>
                            <th scope="col" className="px-6 py-3">
                                Ciudad
                            </th>
                            <th scope="col" className="px-6 py-3">
                                Region
                            </th>
                            <th scope="col" className="px-6 py-3">
                                Acciones
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            sucursales.map(sucursal => (
                                <tr key={sucursal[0]} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                                    <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                        {sucursal[1]}
                                    </th>
                                    <td className="px-6 py-4">
                                        {sucursal[2]}
                                    </td>
                                    <td className="px-6 py-4">
                                        {sucursal[3]}
                                    </td>
                                    <td className="px-6 py-4">
                                        <button onClick={() => editaSuc(sucursal)} className='bg-yellow-600 p-2 rounded-lg text-white font-bold mr-2'>
                                            Editar
                                        </button>
                                        <button onClick={() => deleteSuc(sucursal)} className='bg-red-600 p-2 rounded-lg text-white font-bold mr-2'>
                                            Borrar
                                        </button>
                                    </td>
                                </tr>
                            ))
                        }
                        
                        
                    </tbody>
                </table>
            </div>
                ) : (
                    <Formik
                        initialValues={initialValues}
                        validationSchema={validationSchema}
                        onSubmit={handleSubmit}
                    >
                        {({ errors, touched }) => (
                        <Form>
                            <div className="grid md:grid-cols-2 md:gap-6">
                                <div className="relative z-0 w-full mb-6 group">
                                    <Field type="text" name="idSucursal" id="idSucursal" className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " required />
                                    <label for="idSucursal" className="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Id sucursal</label>
                                    <ErrorMessage component="div" className='text-white' name='idSucursal'/>
                                </div>
                                <div className="relative z-0 w-full mb-6 group">
                                    <Field type="text" name="nombre" id="nombre" className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " required />
                                    <label for="nombre" className="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Nombre</label>
                                    <ErrorMessage component="div" className='text-white' name='nombre'/>
                                </div>
                            </div>
                            <div className="grid md:grid-cols-3 md:gap-6">
                                <div className="relative z-0 w-full mb-6 group">
                                    <Field type="text" name="ciudad" id="ciudad" className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " required />
                                    <label for="ciudad" className="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Ciudad</label>
                                    <ErrorMessage component="div" className='text-white' name='ciudad'/>
                                </div>
                                <div className="relative z-0 w-full mb-6 group">
                                    <Field type="text" name="region" id="region" className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " required />
                                    <label for="region" className="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Region</label>
                                    <ErrorMessage component="div" className='text-white' name='region'/>
                                </div>
                                <div className="relative z-0 w-full mb-6 group">
                                    <Field type="text" name="activos" id="activos" className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " required />
                                    <label for="activos" className="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Activos</label>
                                    <ErrorMessage component="div" className='text-white' name='activos'/>
                                </div>
                            </div>
                            <button type="submit" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Guardar</button>
                        </Form>
                        )}
                    </Formik>
                )
            }
            

        </div>
    )
}

export default TablaSucursales;