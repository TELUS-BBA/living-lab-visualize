import React from 'react';
import Input from '@tds/core-input';
import Box from '@tds/core-box';
import Select from '@tds/core-select';

class Bandwidth extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      test_type: "bandwidth",
    };
  }

  render() {
    return (
      <div>
        <Input label="NanoPi ID" />
        <Input label="Upload Date Month (Exact)" />
        <Input label="Upload Date Month Less Than" />
        <Input label="Upload Date Month Greater Than" />
        <Input label="Upload Date Day (Exact)" />
        <Input label="Upload Date Day Less Than" />
        <Input label="Upload Date Day Greater Than" />
        <Input label="Upload Date Hour (Exact)" />
        <Input label="Upload Date Hour Less Than" />
        <Input label="Upload Date Hour Greater Than" />
        <Input label="Upload Date Minute (Exact)" />
        <Input label="Upload Date Minute Less Than" />
        <Input label="Upload Date Minute Greater Than" />
        <Input label="Bandwidth (Exact)" />
        <Input label="Bandwidth Less Than" />
        <Input label="Bandwidth Greater Than" />
      </div>
    );
  }
}

export default Bandwidth;
