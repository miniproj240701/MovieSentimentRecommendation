import React, { useState } from 'react';
import styled from 'styled-components';
import SearchIcon from '@material-ui/icons/Search';

interface SearchProps {
  initialSearchText?: string;
  searchType?: 'button' | 'combobox';
  options?: string[];
  onSearch?: (searchTerm: string) => void;
}

const Search: React.FC<SearchProps> = ({ initialSearchText = '', searchType = 'button', options = [], onSearch = () => {} }) => {
  const [searchTerm, setSearchTerm] = useState(initialSearchText);

  const handleSearchSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch?.(searchTerm);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <SearchContainer>
      {searchType === 'combobox' ? (
        <SearchForm onSubmit={handleSearchSubmit}>
          <ComboBox>
            <ComboBoxInput
              type="text"
              value={searchTerm}
              onChange={handleInputChange}
              placeholder={initialSearchText}
            />
            {options.length > 0 && (
              <ComboBoxDropdown>
                {options.map((option, index) => (
                  <ComboBoxOption
                    key={index}
                    onClick={() => setSearchTerm(option)}
                  >
                    {option}
                  </ComboBoxOption>
                ))}
              </ComboBoxDropdown>
            )}
            <StyledSearchIcon />
          </ComboBox>
        </SearchForm>
      ) : (
        <SearchButton onClick={() => onSearch(searchTerm)}>
          <SearchText>{searchTerm}</SearchText>
          <StyledSearchIcon />
        </SearchButton>
      )}
    </SearchContainer>
  );
};

const SearchContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  align-items: center;
  width: 100%;
`;

const SearchForm = styled.form`
  display: flex;
  align-items: center;
`;

const ComboBox = styled.div`
  position: relative;
  width: 250px;
  height: 47px;
  display: flex;
  align-items: center;
  background-color: #464646;
  border-radius: 5px;
  padding-right: 10px;
`;

const ComboBoxInput = styled.input`
  width: 100%;
  padding-left: 25px;
  border: none;
  background-color: transparent;
  color: white;
  font-family: 'S-Core Dream', sans-serif;
  font-size: 18px;
  height: 100%;
  border-radius: 5px;

  &::placeholder {
    color: #9e9e9e;
  }

  &:focus {
    outline: none;
    background-color: #555555;
  }
`;

const ComboBoxDropdown = styled.div`
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: #464646;
  border-radius: 0 0 5px 5px;
  overflow: hidden;
  display: none;

  ${ComboBox}:focus-within & {
    display: block;
  }
`;

const ComboBoxOption = styled.div`
  padding: 12px 16px;
  color: white;
  cursor: pointer;

  &:hover {
    background-color: #555555;
  }
`;

const SearchButton = styled.button`
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #464646;
  width: 250px;
  height: 47px;
  border-radius: 5px;
  padding: 0 10px;
  cursor: pointer;
  border: none;

  &:hover {
    background-color: #555555;
  }
`;

const SearchText = styled.span`
  color: white;
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 500;
  font-size: 18px;
  margin-right: 10px;
`;

const StyledSearchIcon = styled(SearchIcon)`
  color: white;
`;

export default Search;
