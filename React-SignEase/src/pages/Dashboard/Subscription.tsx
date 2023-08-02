import React, { ChangeEvent, useState, useRef } from 'react';
import axios from 'axios';
import Breadcrumb from '../../components/Breadcrumb';
import SwitcherThree from '../../components/SwitcherThree';

const Subscription = () => {
  return (
    <>
      <Breadcrumb pageName="Subscription Plans:" />

      <div className='relative'>
        {/* Background Decoration */}
        <div className='absolute inset-0 flex flex-col'>
          <div className='flex-1'></div>
          <div className='bg-meta-19 flex-1 dark:bg-boxdark-2'></div>
        </div>

        <div className="mx-auto grid max-w-7xl gap-12 py-24 px-4 sm:px-6 lg:grid-cols-3 lg:gap-8 lg:px-8">
          <div className="relative flex flex-col rounded-2xl border-slate-200 bg-white p-8 shadow-plan-box shadow-lg flex-col plan-box hover:shadow-lg">

            {/* <------  Free Plan ------> */}
            <h3 className="mb-3 block text-lg font-semibold leading-5 text-black">
              Free
            </h3>
            <p className='mt-4 text-slate-700 dark:text-meta-17'>The essentials to provide your best work for daily usage.</p>

            {/* Price */}
            <div className='-mx-6 mt-4 rounded-lg bg-slate-50 p-6'>
              <p className='flex items-center text-sm font-semibold text-slate-500 dark:text-black'>
                <span>SGD</span>
                <span className='ml-3 text-4xl text-slate-900'>$0</span>
                <span className='ml-1.5'>/month</span>
              </p>
            </div>

            {/* Features */}
            <ul className='mt-6 space-y-4 text-black flex-1'>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Access to Gesture Recognition only</span>
              </li>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Sign Language Dictionary</span>
              </li>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Translation History</span>
              </li>
            </ul>

            {/* Call to Action */}
            <a href='#' className='mt-8 block bg-meta-16 px-6 py-4 text-center text-sm font-semibold leading-4 text-meta-15 hover:bg-meta-15 hover:text-white rounded-lg shadow-md'>
              Start your trial
            </a>
          </div>

          {/* <------  Premium Plan ------> */}
          <div className="relative flex flex-col rounded-2xl border-slate-200 bg-white p-8 shadow-plan-box shadow-lg flex-col plan-box hover:shadow-lg">
            <h3 className="mb-3 block text-lg font-semibold leading-5 text-black">
              Premium
            </h3>
            <p className='absolute top-0 -translate-y-1/2 rounded-full bg-meta-14 px-3 py-0.5 text-sm font-semibold tracking-wide text-white shadow-md'>
              Most popular
            </p>
            <p className='mt-4 text-slate-700 dark:text-meta-17'>A plan that scales with your rapidly growing demand and usage.</p>

            {/* Price */}
            <div className='-mx-6 mt-4 rounded-lg bg-slate-50 p-6'>
              <p className='flex items-center text-sm font-semibold text-slate-500 dark:text-black'>
                <span>SGD</span>
                <span className='ml-3 text-4xl text-slate-900'>$8</span>
                <span className='ml-1.5'>/month</span>
              </p>
            </div>

            {/* Features */}
            <ul className='mt-6 space-y-4 text-black flex-1'>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Access to both Gesture and Action Recognition</span>
              </li>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Sign Language Dictionary</span>
              </li>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Translation History</span>
              </li>
            </ul>

            {/* Call to Action */}
            <a href='#' className='mt-8 block bg-meta-14 px-6 py-4 text-center text-sm font-semibold leading-4 text-white hover:bg-meta-15 rounded-lg shadow-md'>
              Buy Now
            </a>
          </div>

          {/* <------  Enterprise Plan ------> */}
          <div className="relative flex flex-col rounded-2xl border-slate-200 bg-white p-8 shadow-lg flex-col">
            <h3 className="mb-3 block text-lg font-semibold leading-5 text-black">
              Enterprise
            </h3>
            <p className='mt-4 text-slate-700 dark:text-meta-17'>The essentials to provide your best work for clients.</p>

            {/* Price */}
            <div className='-mx-6 mt-4 rounded-lg bg-slate-50 p-6'>
              <p className='flex items-center text-sm font-semibold text-slate-500 dark:text-black'>
                <span>SGD</span>
                <span className='ml-3 text-4xl text-slate-900'>$15</span>
                <span className='ml-1.5'>/month</span>
              </p>
            </div>

            {/* Features */}
            <ul className='mt-6 space-y-4 text-black flex-1'>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Access to both Gesture and Action Recognition</span>
              </li>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Sign Language Dictionary</span>
              </li>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Translation History</span>
              </li>
              <li className='flex leading-6 text-slate-700 items-center'>
                <svg className="h-5 w-5 text-cyan-500 shrink-0 self-start" viewBox="0 0 20 20" fill="#39b1bf" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6.70711 10.2929C6.31658 9.90237 5.68342 9.90237 5.29289 10.2929C4.90237 10.6834 4.90237 11.3166 5.29289 11.7071L6.70711 10.2929ZM14.0784 7.74974C14.4925 7.38427 14.5319 6.75234 14.1664 6.33827C13.801 5.9242 13.169 5.8848 12.755 6.25026L14.0784 7.74974ZM8.84768 13.8477L8.14057 14.5548C8.38489 14.7991 8.73803 14.9 9.07455 14.8216C9.41106 14.7432 9.68327 14.4967 9.79447 14.1695L8.84768 13.8477ZM9.79447 14.1695C10.6447 11.6685 12.1378 9.46254 14.0784 7.74974L12.755 6.25026C10.5581 8.18922 8.86547 10.6883 7.90089 13.5258L9.79447 14.1695ZM5.29289 11.7071L8.14057 14.5548L9.55478 13.1406L6.70711 10.2929L5.29289 11.7071Z" />
                </svg>
                <span className="ml-3">Comes with an Additional Driver! <br></br>(Can be embedded into software such as Zoom or MsTeams)</span>
              </li>
            </ul>

            {/* Call to Action */}
            <a href='#' className='mt-8 block bg-meta-16 px-6 py-4 text-center text-sm font-semibold leading-4 text-meta-15 hover:bg-meta-15 hover:text-white rounded-lg shadow-md'>
              Buy Now
            </a>
          </div>
        </div>
      </div>
    </>
  );
};

export default Subscription;
