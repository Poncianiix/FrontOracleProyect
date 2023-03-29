import React, {useEffect, useState} from 'react'
import axios from "axios";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import swal from 'sweetalert2';

const TablaPrestamos = () => {
    const [agrega, setAgrega] = useState(false)
    const [sucursales, setSucursales] = useState([]);
    const [prestamos, setprestamos] = useState([]);
    const [sucursalactiv, setSucursalactiv] = useState('true');
    useEffect(() => {
        //console.log('cambie');
        if (!agrega)
            obtenerdatos();
    }, [sucursalactiv])

    const obtenerdatos = async() => {
        
        const config = {
            method: 'GET',
            url: 'http://localhost:4000/sucursales/',
            headers: {
              'Content-Type': 'application/json'
            }
        };

        const config2 = {
            method: 'GET',
            url: `${sucursalactiv === 'true' ? ('http://localhost:4000/prestamos') : ('http://localhost:4000/prestamos/sucursal/sucursal')}`,
            headers: {
              'Content-Type': 'application/json'
            }
        };
    
    
        const response = await axios(config);
        const response2 = await axios(config2);
        //console.log(response.data);
        setSucursales(response.data);
        console.log(response2.data);
        setprestamos(response2.data);
    }

    const initialValues = {
        sucursal: '',
        noPrestamo: '',
        cantidad: ''
    }

    const validationSchema = Yup.object().shape({
        sucursal: Yup.string().required('La sucursal es obligatoria'),
        noPrestamo: Yup.string().required('El numero es obligatorio'),
        cantidad: Yup.number().required('La cantidad es obligatoria')
    })

    const handleSubmit = async(values, { resetForm }) => {
        try {
            const config = {
                method: 'POST',
                url: 'http://localhost:4000/prestamos/',
                data: {
                    noprestamo: values.noPrestamo,
                    idsucursal: values.sucursal,
                    cantidad: values.cantidad
                },
                headers: {
                  'Content-Type': 'application/json'
                }
              };   
              const response = await axios(config);

                resetForm();
                obtenerdatos();
                setAgrega(false);
        } catch (error) {
        console.log(error);
        }
    }

    const deletePre = async(pre) => {
        swal.fire({
            title: '¿Estás seguro de que deseas eliminar este prestamo?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Eliminar',
            cancelButtonText: 'Cancelar'
        }).then(async(result) => {
            if (result.isConfirmed) {
                try {
                    const config = {
                        method: 'DELETE',
                        url: `http://localhost:4000/prestamos/${pre[0]}`,
                        data: {
                            idsucursal: pre[1],
                            cantidad: pre[2]
                        },
                        headers: {
                        'Content-Type': 'application/json'
                        }
                    };

                    const response = await axios(config);
                    obtenerdatos();

                    swal.fire(
                        '¡Eliminado!',
                        'El prestamo ha sido eliminado.',
                        'success'
                    );
                } catch (error) {
                    console.log(error);
                }
                
            }
        });
        
    }


    const editaPre = (pre) => {
        swal.fire({
            title: 'Ingrese los datos del prestamo',
            html:
              '<label for="cantidad">Cantidad:</label>' +
              `<input id="cantidad" class="swal2-input" value="${pre[2]}" placeholder="Cantidad">` ,
                focusConfirm: false,
            preConfirm: () => {
              return {
                cantidad: document.getElementById('cantidad').value
              }
            }
          }).then(async(result) => {
            // Aquí puedes usar los valores ingresados en los inputs
            console.log(result.value);
            try {
                const config = {
                    method: 'PUT',
                    url: `http://localhost:4000/prestamos/${pre[0]}`,
                    data: {
                        idsucursal: pre[1],
                        cantidad: result.value.cantidad
                    },
                    headers: {
                    'Content-Type': 'application/json'
                    }
                };

                const response = await axios(config);
                obtenerdatos();
                swal.fire(
                    'Actualizada!',
                    'El prestamo ha sido actualizada.',
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
                    <div className='flex justify-between mb-2'>
                        <select id="countries" onChange={(e) => setSucursalactiv(e.target.value)} class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-1/4 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                            <option selected value={true}>Pretamos completos</option>
                            <option value={false}>Prestamos por sucursal</option>
                            
                        </select>
                        <button onClick={() => setAgrega(true)} className='text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800'>Agregar Prestamo</button>
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
                            {
                                sucursalactiv === 'true' ? 
                                (
                                    <th scope="col" className="px-6 py-3">
                                        Numero
                                    </th>
                                ) : 
                                ('')
                            }
                            
                            <th scope="col" className="px-6 py-3">
                                Sucursal
                            </th>
                            <th scope="col" className="px-6 py-3">
                                Prestamo
                            </th>
                            <th scope="col" className="px-6 py-3">
                                Acciones
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            prestamos.map(prestamo => (
                                <tr key={prestamo[0]} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                                    <th scope="row" className="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                        {prestamo[0]}
                                    </th>
                                    <td className="px-6 py-4">
                                        {prestamo[1]}
                                    </td>
                                    {
                                        sucursalactiv === 'true' ? 
                                        (
                                            <td className="px-6 py-4">
                                                {prestamo[2]}
                                            </td>
                                        ) :
                                        ('')
                                    }
                                    {
                                        sucursalactiv === 'true' ? 
                                        (
                                            <td className="px-6 py-4">
                                                <button onClick={() => editaPre(prestamo)} className='bg-yellow-600 p-2 rounded-lg text-white font-bold mr-2'>
                                                    Editar
                                                </button>
                                                <button onClick={() => deletePre(prestamo)} className='bg-red-600 p-2 rounded-lg text-white font-bold mr-2'>
                                                    Borrar
                                                </button>
                                            </td>
                                        ) :
                                        (
                                            ''
                                        )
                                    }
                                    
                                    
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
                            <div class="relative z-0 w-full mb-6 group">
                                <label for="underline_select" class="sr-only">Underline select</label>
                                <Field as="select" name="sucursal" id='sucursal' className="block py-2.5 px-0 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none dark:text-gray-400 dark:border-gray-700 focus:outline-none focus:ring-0 focus:border-gray-200 peer">
                                    <option selected>Selecciona una sucursal</option>
                                    {
                                        sucursales.map(sucursal => (
                                            <option value={sucursal[0]}>{sucursal[1]}</option>
                                        ))
                                    }
                                </Field>
                                <ErrorMessage component="div" className='text-white' name='sucursal'/>
                            </div>
                            <div className="grid md:grid-cols-2 md:gap-6">
                                <div className="relative z-0 w-full mb-6 group">
                                    <Field type="text" name="noPrestamo" id="noPrestamo" className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " required />
                                    <label for="noPrestamo" className="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Numero Prestamos</label>
                                    <ErrorMessage component="div" className='text-white' name='noPrestamo'/>
                                </div>
                                <div className="relative z-0 w-full mb-6 group">
                                    <Field type="text" name="cantidad" id="cantidad" className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" placeholder=" " required />
                                    <label for="cantidad" className="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">cantidad</label>
                                    <ErrorMessage component="div" className='text-white' name='cantidad'/>
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




export default TablaPrestamos;