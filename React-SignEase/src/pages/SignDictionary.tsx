import React, { useState, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import Select from 'react-select';
import { ErrorMessage } from "@hookform/error-message";
import Breadcrumb from '../components/Breadcrumb';
import * as alphabetImages from '../images/asl_alphabets'; // update with your actual path

interface ImageDictionary {
  [key: string]: string;
}

// Cast alphabetImages to the new type
const images: ImageDictionary = alphabetImages as ImageDictionary;

const SignDictionary = () => {
  const { handleSubmit, control, formState: { errors } } = useForm();
  const [selectedType, setSelectedType] = useState('');
  const [selectedAlphabet, setSelectedAlphabet] = useState('');

  useEffect(() => {
    if (selectedType === 'Alphabets' && selectedAlphabet !== '') {
      // The alphabet image will be updated every time selectedType and selectedAlphabet change
    }
  }, [selectedType, selectedAlphabet]);

  const categoryOptions = selectedType === 'Alphabets' ?
    Array.from({ length: 26 }, (_, i) => String.fromCharCode(i + 65)).map(letter => ({ value: letter, label: letter }))
    : [{ value: 'please', label: 'Please' }, { value: 'review', label: 'Review' }, { value: 'bug', label: 'Bug' }, { value: 'and', label: 'And' }, { value: 'change', label: 'Change' }, { value: 'code', label: 'Code' }, { value: 'integrate', label: 'Integrate' }, { value: 'commit', label: 'Commit' }, { value: 'fix', label: 'Fix' }, { value: 'pull', label: 'Pull' }, { value: 'request', label: 'Request' }, { value: 'Test', label: 'Test' }]; 

  return (
    <>
      <div className="mx-auto max-w-270">
        <Breadcrumb pageName="Sign Language Dictionary" />

        <form onSubmit={handleSubmit((data) => console.log(data))}>
          <div className="flex space-x-4">
            <div className="w-1/2">
              <Controller
                name="signType"
                control={control}
                rules={{ required: "This is required" }}
                render={({ field }) => (
                  <Select
                    {...field}
                    className="w-full"
                    options={[{ value: 'Alphabets', label: 'Alphabets' }, { value: 'Words', label: 'Words' }]}
                    onChange={(option) => { setSelectedType(option.value); field.onChange(option); }}
                  />
                )}
              />
            </div>

            <div className="w-1/2">
              <Controller
                name="category"
                control={control}
                rules={{ required: "This is required" }}
                render={({ field }) => (
                  <Select
                    {...field}
                    className="w-full"
                    options={categoryOptions}
                    onChange={(option) => { setSelectedAlphabet(option.value); field.onChange(option); }}
                  />
                )}
              />
            </div>
          </div>
        </form>
        
        {selectedType === 'Alphabets' && selectedAlphabet &&
          <div className="flex justify-center items-center mt-18">  {/* Added margin top (mt-4) here */}
            <img className="w-1/2 h-auto" src={images[selectedAlphabet]} alt={selectedAlphabet} />
          </div>

        }
      </div>
    </>
  );
};

export default SignDictionary;
