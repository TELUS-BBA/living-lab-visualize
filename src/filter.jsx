import React from 'react';
import Box from '@tds/core-box';
import Select from '@tds/core-select';

import Bandwidth from './bandwidth';
import Jitter from './jitter';
import Latency from './latency';
import Ping from './ping';

class Filter extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      test_type: "bandwidth",
    };
  }

  render() {
    return (
      <Box inset={1} between={2}>
        <Select
          label="Test Type"
          placeholder="Select test type..."
          value={this.state.test_type}
          options={[
            { text: 'Bandwidth', value: 'bandwidth' },
            { text: 'Jitter', value: 'jitter' },
            { text: 'One-Way Latency', value: 'sockperf' },
            { text: 'Ping', value: 'ping' },
          ]}
          onChange={ (event) => { this.setState({test_type: event.target.value}); }}
        />
        { this.state.test_type === 'bandwidth' &&
            <Bandwidth />
        }
        { this.state.test_type === 'jitter' &&
            <Jitter />
        }
        { this.state.test_type === 'sockperf' &&
            <Latency />
        }
        { this.state.test_type === 'ping' &&
            <Ping />
        }
      </Box>
    );
  }
}

export default Filter;
