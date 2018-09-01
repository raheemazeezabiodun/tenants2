import { formatErrors, getFormErrors } from "../form-errors";
import { shallow } from "enzyme";
import { assertNotNull } from "../util";

describe('formatErrors()', () => {
  it('concatenates errors', () => {
    const { errorHelp } = formatErrors({
      errors: ['foo', 'bar']
    });
    expect(shallow(assertNotNull(errorHelp)).html())
      .toBe('<p class="help is-danger">foo, bar</p>');
  });

  it('returns null for errorHelp when no errors exist', () => {
    expect(formatErrors({}).errorHelp).toBeNull();
  });

  it('creates an ariaLabel', () => {
    expect(formatErrors({
      errors: ['this field is required'],
      label: 'Name'
    }).ariaLabel).toBe('Name, this field is required');
  });
});

describe('getFormErrors()', () => {
  it('works with an empty array', () => {
    expect(getFormErrors([])).toEqual({
      nonFieldErrors: [],
      fieldErrors: {}
    });
  });

  it('sets nonFieldErrors', () => {
    expect(getFormErrors([{
      field: '__all__',
      messages: ['foo', 'bar']  
    }])).toEqual({
      nonFieldErrors: ['foo', 'bar'],
      fieldErrors: {}
    });
  });

  it('sets fieldErrors', () => {
    expect(getFormErrors([{
      field: 'boop',
      messages: ['foo', 'bar']  
    }])).toEqual({
      nonFieldErrors: [],
      fieldErrors: {
        boop: ['foo', 'bar']
      }
    });
  });

  it('combines multiple field error messages', () => {
    expect(getFormErrors([{
      field: 'boop',
      messages: ['foo']
    }, {
      field: 'boop',
      messages: ['bar']
    }])).toEqual({
      nonFieldErrors: [],
      fieldErrors: {
        boop: ['foo', 'bar']
      }
    });
  });
});
