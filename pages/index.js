import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import React, {useState, useEffect} from 'react'
import TablaSucursales from '../components/TablaSucursales';
import TablaPrestamos from '../components/TablaPrestamos';
export default function Home() {

  const [sucursales, setSucursales] = useState(true);

  return (
    <div className={styles.container}>
      <Head>
        <title>Sucursales y prestamos</title>
        <meta name="description" content="Generated by create next app" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

    <div className='px-10'>
      <div className="text-sm font-medium text-center text-gray-500 border-b border-gray-200 dark:text-gray-400 dark:border-gray-700">
          <ul className="flex flex-wrap -mb-px">
              <li className="mr-2">
                  <a onClick={() => setSucursales(true)} className={!sucursales ? ("inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300") : ("inline-block p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active dark:text-blue-500 dark:border-blue-500")}>Sucursales</a>
              </li>
              <li className="mr-2">
                  <a onClick={() => setSucursales(false)} className={sucursales ? ("inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300") : ("inline-block p-4 text-blue-600 border-b-2 border-blue-600 rounded-t-lg active dark:text-blue-500 dark:border-blue-500")} aria-current="page">Prestamos</a>
              </li>
          </ul>
      </div>
      {
        sucursales ?<TablaSucursales/> : <TablaPrestamos/>
      }
    </div>



      <footer className={styles.footer}>
        <a
          href="https://github.com/Poncianiix/FrontOracleProyect.git"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <span className={styles.logo}>
            Los castores del norte
          </span>
        </a>
      </footer>
    </div>
  )
}
