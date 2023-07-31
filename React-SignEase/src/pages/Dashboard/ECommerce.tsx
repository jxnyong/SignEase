import React, { ChangeEvent, useState, useRef } from 'react';
import axios from 'axios';
import Breadcrumb from '../../components/Breadcrumb';
import SwitcherThree from '../../components/SwitcherThree';

const ECommerce = () => {
  return (
    <>
      <Breadcrumb pageName="Subscription" />

      <div className="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="flex flex-col gap-5.5 p-6.5">
          <div className="mb-5.5 mt-10 flex flex-col gap-5.5 sm:flex-row">
            <div className="w-full sm:w-1/3">
              <label className="mb-3 block text-black dark:text-white">
                Free
              </label>
              <textarea
                rows={6}
                placeholder="- Only access to gesture recognition"
                className="w-full rounded-lg border-[1.5px] text-black border-strokewhite bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                readOnly
              ></textarea>
            </div>

            <div className="w-full sm:w-1/3">
              <label className="mb-3 block text-black dark:text-white">
                Premium
              </label>
              <textarea
                rows={6}
                placeholder="- Access to both gesture and action recogition"
                className="w-full rounded-lg border-[1.5px] text-black border-strokewhite bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                readOnly
              ></textarea>
            </div>

            <div className="w-full sm:w-1/3">
              <label className="mb-3 block text-black dark:text-white">
                Level 2 Subscription
              </label>
              <textarea
                rows={6}
                placeholder="- Access to all functionality"
                className="w-full rounded-lg border-[1.5px] text-black border-strokewhite bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                readOnly
              ></textarea>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ECommerce;
