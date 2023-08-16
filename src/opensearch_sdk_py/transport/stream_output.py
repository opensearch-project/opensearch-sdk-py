from opensearch_sdk_py.transport.version import Version

class StreamOutput:
    def __init__(self, loop, sock):
      self.loop = loop
      self.sock = sock
    
    def write(self, b: bytes):
        return self.loop.sock_sendall(self.sock, b)

    #  writes an int as four bytes.
    def write_int(self, i: int):
        return self.write(i.to_bytes(4, byteorder='big'))

    # writes an int in a variable-length format
    def write_v_int(self, i: int):
        result = ''
        while True:
            result = chr((i & 0x7f) | 0x80) + result
            i >>= 7
            if ((i & ~0x7F) == 0):
                break
        return self.write(result)
      
    # writes the OpenSearch {@link Version} to the output stream
    def write_version(self, version: Version):
        return self.write_v_int(version.id)

    # }
    # /**
    #  Writes an array of bytes.
    #      #  @param b the bytes to write
    #  
    # def write_byteArray(byte[] b) throws IOException {
    #     writeVInt(b.length);
    #     write_bytes(b, 0, b.length);
    # }

    # /**
    #  Writes the bytes reference, including a length header.
    #  
    # def write_bytesReference(@Nullable BytesReference bytes) throws IOException {
    #     if (bytes == null) {
    #         writeVInt(0);
    #         return;
    #     }
    #     writeVInt(bytes.length());
    #     bytes.writeTo(this);
    # }

    # /**
    #  Writes an optional bytes reference including a length header. Use this if you need to differentiate between null and empty bytes
    #  references. Use {@link #write_bytesReference(BytesReference)} and {@link StreamInput#readBytesReference()} if you do not.
    #  
    # def writeOptionalBytesReference(@Nullable BytesReference bytes) throws IOException {
    #     if (bytes == null) {
    #         writeVInt(0);
    #         return;
    #     }
    #     writeVInt(bytes.length() + 1);
    #     bytes.writeTo(this);
    # }

    # def write_bytesRef(BytesRef bytes) throws IOException {
    #     if (bytes == null) {
    #         writeVInt(0);
    #         return;
    #     }
    #     writeVInt(bytes.length);
    #     write(bytes.bytes, bytes.offset, bytes.length);
    # }

    # private static final ThreadLocal<byte[]> scratch = ThreadLocal.withInitial(() -> new byte[1024]);

    # public final void writeShort(short v) throws IOException {
    #     final byte[] buffer = scratch.get();
    #     buffer[0] = (byte) (v >> 8);
    #     buffer[1] = (byte) v;
    #     write_bytes(buffer, 0, 2);
    # }



    # /**
    #  Writes a long as eight bytes.
    #  
    # def writeLong(long i) throws IOException {
    #     final byte[] buffer = scratch.get();
    #     buffer[0] = (byte) (i >> 56);
    #     buffer[1] = (byte) (i >> 48);
    #     buffer[2] = (byte) (i >> 40);
    #     buffer[3] = (byte) (i >> 32);
    #     buffer[4] = (byte) (i >> 24);
    #     buffer[5] = (byte) (i >> 16);
    #     buffer[6] = (byte) (i >> 8);
    #     buffer[7] = (byte) i;
    #     write_bytes(buffer, 0, 8);
    # }

    # /**
    #  Writes a non-negative long in a variable-length format. Writes between one and ten bytes. Smaller values take fewer bytes. Negative
    #  numbers use ten bytes and trip assertions (if running in tests) so prefer {@link #writeLong(long)} or {@link #writeZLong(long)} for
    #  negative numbers.
    #  
    # def writeVLong(long i) throws IOException {
    #     if (i < 0) {
    #         throw new IllegalStateException("Negative longs unsupported, use writeLong or writeZLong for negative numbers [" + i + "]");
    #     }
    #     writeVLongNoCheck(i);
    # }

    # def writeOptionalVLong(@Nullable Long l) throws IOException {
    #     if (l == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeVLong(l);
    #     }
    # }

    # /**
    #  Writes a long in a variable-length format without first checking if it is negative. Package private for testing. Use
    #  {@link #writeVLong(long)} instead.
    #  
    # def writeVLongNoCheck(long i) throws IOException {
    #     final byte[] buffer = scratch.get();
    #     int index = 0;
    #     while ((i & ~0x7F) != 0) {
    #         buffer[index++] = ((byte) ((i & 0x7f) | 0x80));
    #         i >>>= 7;
    #     }
    #     buffer[index++] = ((byte) i);
    #     write_bytes(buffer, 0, index);
    # }

    # /**
    #  Writes a long in a variable-length format. Writes between one and ten bytes.
    #  Values are remapped by sliding the sign bit into the lsb and then encoded as an unsigned number
    #  e.g., 0 -;&gt; 0, -1 -;&gt; 1, 1 -;&gt; 2, ..., Long.MIN_VALUE -;&gt; -1, Long.MAX_VALUE -;&gt; -2
    #  Numbers with small absolute value will have a small encoding
    #  If the numbers are known to be non-negative, use {@link #writeVLong(long)}
    #  
    # def writeZLong(long i) throws IOException {
    #     final byte[] buffer = scratch.get();
    #     int index = 0;
    #     // zig-zag encoding cf. https://developers.google.com/protocol-buffers/docs/encoding?hl=en
    #     long value = BitUtil.zigZagEncode(i);
    #     while ((value & 0xFFFFFFFFFFFFFF80L) != 0L) {
    #         buffer[index++] = (byte) ((value & 0x7F) | 0x80);
    #         value >>>= 7;
    #     }
    #     buffer[index++] = (byte) (value & 0x7F);
    #     write_bytes(buffer, 0, index);
    # }

    # def writeOptionalLong(@Nullable Long l) throws IOException {
    #     if (l == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeLong(l);
    #     }
    # }

    # def writeOptionalString(@Nullable String str) throws IOException {
    #     if (str == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeString(str);
    #     }
    # }

    # def writeOptionalSecureString(@Nullable SecureString secureStr) throws IOException {
    #     if (secureStr == null) {
    #         writeOptionalBytesReference(null);
    #     } else {
    #         final byte[] secureStrBytes = CharArrays.toUtf8Bytes(secureStr.getChars());
    #         try {
    #             writeOptionalBytesReference(new BytesArray(secureStrBytes));
    #         } finally {
    #             Arrays.fill(secureStrBytes, (byte) 0);
    #         }
    #     }
    # }

    # /**
    #  Writes an optional {@link Integer}.
    #  
    # def writeOptionalInt(@Nullable Integer integer) throws IOException {
    #     if (integer == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeInt(integer);
    #     }
    # }

    # def writeOptionalVInt(@Nullable Integer integer) throws IOException {
    #     if (integer == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeVInt(integer);
    #     }
    # }

    # def writeOptionalFloat(@Nullable Float floatValue) throws IOException {
    #     if (floatValue == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeFloat(floatValue);
    #     }
    # }

    # def writeOptionalText(@Nullable Text text) throws IOException {
    #     if (text == null) {
    #         writeInt(-1);
    #     } else {
    #         writeText(text);
    #     }
    # }

    # private final BytesRefBuilder spare = new BytesRefBuilder();

    # def writeText(Text text) throws IOException {
    #     if (!text.hasBytes()) {
    #         final String string = text.string();
    #         spare.copyChars(string);
    #         writeInt(spare.length());
    #         write(spare.bytes(), 0, spare.length());
    #     } else {
    #         BytesReference bytes = text.bytes();
    #         writeInt(bytes.length());
    #         bytes.writeTo(this);
    #     }
    # }

    # def writeString(String str) throws IOException {
    #     final int charCount = str.length();
    #     byte[] buffer = scratch.get();
    #     int offset = 0;
    #     writeVInt(charCount);
    #     for (int i = 0; i < charCount; i++) {
    #         final int c = str.charAt(i);
    #         if (c <= 0x007F) {
    #             buffer[offset++] = ((byte) c);
    #         } else if (c > 0x07FF) {
    #             buffer[offset++] = ((byte) (0xE0 | c >> 12 & 0x0F));
    #             buffer[offset++] = ((byte) (0x80 | c >> 6 & 0x3F));
    #             buffer[offset++] = ((byte) (0x80 | c >> 0 & 0x3F));
    #         } else {
    #             buffer[offset++] = ((byte) (0xC0 | c >> 6 & 0x1F));
    #             buffer[offset++] = ((byte) (0x80 | c >> 0 & 0x3F));
    #         }
    #         // make sure any possible char can fit into the buffer in any possible iteration
    #         // we need at most 3 bytes so we flush the buffer once we have less than 3 bytes
    #         // left before we start another iteration
    #         if (offset > buffer.length - 3) {
    #             write_bytes(buffer, offset);
    #             offset = 0;
    #         }
    #     }
    #     write_bytes(buffer, offset);
    # }

    # def writeSecureString(SecureString secureStr) throws IOException {
    #     final byte[] secureStrBytes = CharArrays.toUtf8Bytes(secureStr.getChars());
    #     try {
    #         write_bytesReference(new BytesArray(secureStrBytes));
    #     } finally {
    #         Arrays.fill(secureStrBytes, (byte) 0);
    #     }
    # }

    # def writeFloat(float v) throws IOException {
    #     writeInt(Float.floatToIntBits(v));
    # }

    # def writeDouble(double v) throws IOException {
    #     writeLong(Double.doubleToLongBits(v));
    # }

    # def writeOptionalDouble(@Nullable Double v) throws IOException {
    #     if (v == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeDouble(v);
    #     }
    # }

    # public final void write_bigInteger(BigInteger v) throws IOException {
    #     writeString(v.toString());
    # }

    # private static byte ZERO = 0;
    # private static byte ONE = 1;
    # private static byte TWO = 2;

    # /**
    #  Writes a boolean.
    #  
    # def write_boolean(boolean b) throws IOException {
    #     write_byte(b ? ONE : ZERO);
    # }

    # def writeOptionalBoolean(@Nullable Boolean b) throws IOException {
    #     if (b == null) {
    #         write_byte(TWO);
    #     } else {
    #         write_boolean(b);
    #     }
    # }

    # /**
    #  Forces any buffered output to be written.
    #  
    # @Override
    # def flush(self, ):
    #     pass

    # /**
    #  Closes this stream to further operations.
    #  
    # @Override
    # def close(self, ):
    #     pass

    # def reset(self, ):
    #     pass

    # @Override
    # def write(int b) throws IOException {
    #     write_byte((byte) b);
    # }

    # @Override
    # def write(byte[] b, int off, int len) throws IOException {
    #     write_bytes(b, off, len);
    # }

    # def writeStringArray(String[] array) throws IOException {
    #     writeVInt(array.length);
    #     for (String s : array) {
    #         writeString(s);
    #     }
    # }

    # /**
    #  Writes a string array, for nullable string, writes it as 0 (empty string).
    #  
    # def writeStringArrayNullable(@Nullable String[] array) throws IOException {
    #     if (array == null) {
    #         writeVInt(0);
    #     } else {
    #         writeVInt(array.length);
    #         for (String s : array) {
    #             writeString(s);
    #         }
    #     }
    # }

    # /**
    #  Writes a string array, for nullable string, writes false.
    #  
    # def writeOptionalStringArray(@Nullable String[] array) throws IOException {
    #     if (array == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeStringArray(array);
    #     }
    # }

    # def writeMap(@Nullable Map<String, Object> map) throws IOException {
    #     writeGenericValue(map);
    # }

    # /**
    #  write map to stream with consistent order
    #  to make sure every map generated bytes order are same.
    #  This method is compatible with {@code StreamInput.readMap} and {@code StreamInput.readGenericValue}
    #  This method only will handle the map keys order, not maps contained within the map
    #  
    # def writeMapWithConsistentOrder(@Nullable Map<String, ? extends Object> map) throws IOException {
    #     if (map == null) {
    #         write_byte((byte) -1);
    #         return;
    #     }
    #     assert false == (map instanceof LinkedHashMap);
    #     this.write_byte((byte) 10);
    #     this.writeVInt(map.size());
    #     Iterator<? extends Map.Entry<String, ?>> iterator = map.entrySet()
    #         .stream()
    #         .sorted((a, b) -> a.getKey().compareTo(b.getKey()))
    #         .iterator();
    #     while (iterator.hasNext()) {
    #         Map.Entry<String, ?> next = iterator.next();
    #         this.writeString(next.getKey());
    #         this.writeGenericValue(next.getValue());
    #     }
    # }

    # /**
    #  Write a {@link Map} of {@code K}-type keys to {@code V}-type {@link List}s.
    #  <pre><code>
    #  Map&lt;String, List&lt;String&gt;&gt; map = ...;
    #  out.writeMapOfLists(map, StreamOutput::writeString, StreamOutput::writeString);
    #  </code></pre>
    #      #  @param keyWriter The key writer
    #  @param valueWriter The value writer
    #  
    # public final <K, V> void writeMapOfLists(final Map<K, List<V>> map, final Writer<K> keyWriter, final Writer<V> valueWriter)
    #     throws IOException {
    #     writeMap(map, keyWriter, (stream, list) -> {
    #         writeVInt(list.size());
    #         for (final V value : list) {
    #             valueWriter.write(this, value);
    #         }
    #     });
    # }

    # /**
    #  Write a {@link Map} of {@code K}-type keys to {@code V}-type.
    #  <pre><code>
    #  Map&lt;String, String&gt; map = ...;
    #  out.writeMap(map, StreamOutput::writeString, StreamOutput::writeString);
    #  </code></pre>
    #      #  @param keyWriter The key writer
    #  @param valueWriter The value writer
    #  
    # public final <K, V> void writeMap(final Map<K, V> map, final Writer<K> keyWriter, final Writer<V> valueWriter) throws IOException {
    #     writeVInt(map.size());
    #     for (final Map.Entry<K, V> entry : map.entrySet()) {
    #         keyWriter.write(this, entry.getKey());
    #         valueWriter.write(this, entry.getValue());
    #     }
    # }

    # /**
    #  Writes an {@link Instant} to the stream with nanosecond resolution
    #  
    # public final void writeInstant(Instant instant) throws IOException {
    #     writeLong(instant.getEpochSecond());
    #     writeInt(instant.getNano());
    # }

    # /**
    #  Writes an {@link Instant} to the stream, which could possibly be null
    #  
    # public final void writeOptionalInstant(@Nullable Instant instant) throws IOException {
    #     if (instant == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeInstant(instant);
    #     }
    # }

    # private static final Map<Class<?>, Writer<Object>> WRITERS;

    # static {
    #     Map<Class<?>, Writer<Object>> writers = new HashMap<>();
    #     writers.put(String.class, (o, v) -> {
    #         o.write_byte((byte) 0);
    #         o.writeString((String) v);
    #     });
    #     writers.put(Integer.class, (o, v) -> {
    #         o.write_byte((byte) 1);
    #         o.writeInt((Integer) v);
    #     });
    #     writers.put(Long.class, (o, v) -> {
    #         o.write_byte((byte) 2);
    #         o.writeLong((Long) v);
    #     });
    #     writers.put(Float.class, (o, v) -> {
    #         o.write_byte((byte) 3);
    #         o.writeFloat((float) v);
    #     });
    #     writers.put(Double.class, (o, v) -> {
    #         o.write_byte((byte) 4);
    #         o.writeDouble((double) v);
    #     });
    #     writers.put(Boolean.class, (o, v) -> {
    #         o.write_byte((byte) 5);
    #         o.write_boolean((boolean) v);
    #     });
    #     writers.put(byte[].class, (o, v) -> {
    #         o.write_byte((byte) 6);
    #         final byte[] bytes = (byte[]) v;
    #         o.writeVInt(bytes.length);
    #         o.write_bytes(bytes);
    #     });
    #     writers.put(List.class, (o, v) -> {
    #         o.write_byte((byte) 7);
    #         @SuppressWarnings("rawtypes")
    #         final List list = (List) v;
    #         o.writeVInt(list.size());
    #         for (Object item : list) {
    #             o.writeGenericValue(item);
    #         }
    #     });
    #     writers.put(Object[].class, (o, v) -> {
    #         o.write_byte((byte) 8);
    #         final Object[] list = (Object[]) v;
    #         o.writeVInt(list.length);
    #         for (Object item : list) {
    #             o.writeGenericValue(item);
    #         }
    #     });
    #     writers.put(Map.class, (o, v) -> {
    #         if (v instanceof LinkedHashMap) {
    #             o.write_byte((byte) 9);
    #         } else {
    #             o.write_byte((byte) 10);
    #         }
    #         @SuppressWarnings("unchecked")
    #         final Map<String, Object> map = (Map<String, Object>) v;
    #         o.writeVInt(map.size());
    #         for (Map.Entry<String, Object> entry : map.entrySet()) {
    #             o.writeString(entry.getKey());
    #             o.writeGenericValue(entry.getValue());
    #         }
    #     });
    #     writers.put(Byte.class, (o, v) -> {
    #         o.write_byte((byte) 11);
    #         o.write_byte((Byte) v);
    #     });
    #     writers.put(Date.class, (o, v) -> {
    #         o.write_byte((byte) 12);
    #         o.writeLong(((Date) v).getTime());
    #     });
    #     writers.put(BytesReference.class, (o, v) -> {
    #         o.write_byte((byte) 14);
    #         o.write_bytesReference((BytesReference) v);
    #     });
    #     writers.put(Text.class, (o, v) -> {
    #         o.write_byte((byte) 15);
    #         o.writeText((Text) v);
    #     });
    #     writers.put(Short.class, (o, v) -> {
    #         o.write_byte((byte) 16);
    #         o.writeShort((Short) v);
    #     });
    #     writers.put(int[].class, (o, v) -> {
    #         o.write_byte((byte) 17);
    #         o.writeIntArray((int[]) v);
    #     });
    #     writers.put(long[].class, (o, v) -> {
    #         o.write_byte((byte) 18);
    #         o.writeLongArray((long[]) v);
    #     });
    #     writers.put(float[].class, (o, v) -> {
    #         o.write_byte((byte) 19);
    #         o.writeFloatArray((float[]) v);
    #     });
    #     writers.put(double[].class, (o, v) -> {
    #         o.write_byte((byte) 20);
    #         o.writeDoubleArray((double[]) v);
    #     });
    #     writers.put(BytesRef.class, (o, v) -> {
    #         o.write_byte((byte) 21);
    #         o.write_bytesRef((BytesRef) v);
    #     });
    #     writers.put(ZonedDateTime.class, (o, v) -> {
    #         o.write_byte((byte) 23);
    #         final ZonedDateTime zonedDateTime = (ZonedDateTime) v;
    #         o.writeString(zonedDateTime.getZone().getId());
    #         o.writeLong(zonedDateTime.toInstant().toEpochMilli());
    #     });
    #     writers.put(Set.class, (o, v) -> {
    #         if (v instanceof LinkedHashSet) {
    #             o.write_byte((byte) 24);
    #         } else {
    #             o.write_byte((byte) 25);
    #         }
    #         o.writeCollection((Set<?>) v, StreamOutput::writeGenericValue);
    #     });
    #     // TODO: improve serialization of BigInteger
    #     writers.put(BigInteger.class, (o, v) -> {
    #         o.write_byte((byte) 26);
    #         o.writeString(v.toString());
    #     });
    #     WRITERS = Collections.unmodifiableMap(writers);
    # }

    # private static Class<?> getGenericType(Object value) {
    #     Class<?> registeredClass = WriteableRegistry.getCustomClassFromInstance(value);
    #     if (registeredClass != null) {
    #         return registeredClass;
    #     } else if (value instanceof List) {
    #         return List.class;
    #     } else if (value instanceof Object[]) {
    #         return Object[].class;
    #     } else if (value instanceof Map) {
    #         return Map.class;
    #     } else if (value instanceof Set) {
    #         return Set.class;
    #     } else if (value instanceof BytesReference) {
    #         return BytesReference.class;
    #     } else {
    #         return value.getClass();
    #     }
    # }

    # /**
    #  Notice: when serialization a map, the stream out map with the stream in map maybe have the
    #  different key-value orders, they will maybe have different stream order.
    #  If want to keep stream out map and stream in map have the same stream order when stream,
    #  can use {@code writeMapWithConsistentOrder}
    #  
    # def writeGenericValue(@Nullable Object value) throws IOException {
    #     if (value == null) {
    #         write_byte((byte) -1);
    #         return;
    #     }
    #     final Class<?> type = getGenericType(value);
    #     Writer<Object> writer = WriteableRegistry.getWriter(type);
    #     if (writer == null) {
    #         // fallback to this local hashmap
    #         // todo: move all writers to the registry
    #         writer = WRITERS.get(type);
    #     }
    #     if (writer != null) {
    #         writer.write(this, value);
    #     } else {
    #         throw new IllegalArgumentException("can not write type [" + type + "]");
    #     }
    # }

    # public static void checkWriteable(@Nullable Object value) throws IllegalArgumentException {
    #     if (value == null) {
    #         return;
    #     }
    #     final Class<?> type = getGenericType(value);

    #     if (type == List.class) {
    #         @SuppressWarnings("unchecked")
    #         List<Object> list = (List<Object>) value;
    #         for (Object v : list) {
    #             checkWriteable(v);
    #         }
    #     } else if (type == Object[].class) {
    #         Object[] array = (Object[]) value;
    #         for (Object v : array) {
    #             checkWriteable(v);
    #         }
    #     } else if (type == Map.class) {
    #         @SuppressWarnings("unchecked")
    #         Map<String, Object> map = (Map<String, Object>) value;
    #         for (Map.Entry<String, Object> entry : map.entrySet()) {
    #             checkWriteable(entry.getKey());
    #             checkWriteable(entry.getValue());
    #         }
    #     } else if (type == Set.class) {
    #         @SuppressWarnings("unchecked")
    #         Set<Object> set = (Set<Object>) value;
    #         for (Object v : set) {
    #             checkWriteable(v);
    #         }
    #     } else if (WRITERS.containsKey(type) == false) {
    #         throw new IllegalArgumentException("Cannot write type [" + type.getCanonicalName() + "] to stream");
    #     }
    # }

    # def writeIntArray(int[] values) throws IOException {
    #     writeVInt(values.length);
    #     for (int value : values) {
    #         writeInt(value);
    #     }
    # }

    # def writeVIntArray(int[] values) throws IOException {
    #     writeVInt(values.length);
    #     for (int value : values) {
    #         writeVInt(value);
    #     }
    # }

    # def writeLongArray(long[] values) throws IOException {
    #     writeVInt(values.length);
    #     for (long value : values) {
    #         writeLong(value);
    #     }
    # }

    # def writeVLongArray(long[] values) throws IOException {
    #     writeVInt(values.length);
    #     for (long value : values) {
    #         writeVLong(value);
    #     }
    # }

    # def writeFloatArray(float[] values) throws IOException {
    #     writeVInt(values.length);
    #     for (float value : values) {
    #         writeFloat(value);
    #     }
    # }

    # def writeDoubleArray(double[] values) throws IOException {
    #     writeVInt(values.length);
    #     for (double value : values) {
    #         writeDouble(value);
    #     }
    # }

    # /**
    #  Writes the specified array to the stream using the specified {@link Writer} for each element in the array. This method can be seen as
    #  writer version of {@link StreamInput#readArray(Writeable.Reader, IntFunction)}. The length of array encoded as a variable-length
    #  integer is first written to the stream, and then the elements of the array are written to the stream.
    #      #  @param writer the writer used to write individual elements
    #  @param array  the array
    #  @param <T>    the type of the elements of the array
    #  @throws IOException if an I/O exception occurs while writing the array
    #  
    # public <T> void writeArray(final Writer<T> writer, final T[] array) throws IOException {
    #     writeVInt(array.length);
    #     for (T value : array) {
    #         writer.write(this, value);
    #     }
    # }

    # /**
    #  Same as {@link #writeArray(Writer, Object[])} but the provided array may be null. An additional boolean value is
    #  serialized to indicate whether the array was null or not.
    #  
    # public <T> void writeOptionalArray(final Writer<T> writer, final @Nullable T[] array) throws IOException {
    #     if (array == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeArray(writer, array);
    #     }
    # }

    # /**
    #  Writes the specified array of {@link Writeable}s. This method can be seen as
    #  writer version of {@link StreamInput#readArray(Writeable.Reader, IntFunction)}. The length of array encoded as a variable-length
    #  integer is first written to the stream, and then the elements of the array are written to the stream.
    #  
    # public <T extends Writeable> void writeArray(T[] array) throws IOException {
    #     writeArray((out, value) -> value.writeTo(out), array);
    # }

    # /**
    #  Same as {@link #writeArray(Writeable[])} but the provided array may be null. An additional boolean value is
    #  serialized to indicate whether the array was null or not.
    #  
    # public <T extends Writeable> void writeOptionalArray(@Nullable T[] array) throws IOException {
    #     writeOptionalArray((out, value) -> value.writeTo(out), array);
    # }

    # def writeOptionalWriteable(@Nullable Writeable writeable) throws IOException {
    #     if (writeable != null) {
    #         write_boolean(true);
    #         writeable.writeTo(this);
    #     } else {
    #         write_boolean(false);
    #     }
    # }

    # def writeException(Throwable throwable) throws IOException {
    #     writeException(throwable, throwable, 0);
    # }

    # private void writeException(Throwable rootException, Throwable throwable, int nestedLevel) throws IOException {
    #     if (throwable == null) {
    #         write_boolean(false);
    #     } else if (nestedLevel > MAX_NESTED_EXCEPTION_LEVEL) {
    #         assert failOnTooManyNestedExceptions(rootException);
    #         writeException(new IllegalStateException("too many nested exceptions"));
    #     } else {
    #         write_boolean(true);
    #         boolean writeCause = true;
    #         boolean writeMessage = true;
    #         if (throwable instanceof CorruptIndexException) {
    #             writeVInt(1);
    #             writeOptionalString(((CorruptIndexException) throwable).getOriginalMessage());
    #             writeOptionalString(((CorruptIndexException) throwable).getResourceDescription());
    #             writeMessage = false;
    #         } else if (throwable instanceof IndexFormatTooNewException) {
    #             writeVInt(2);
    #             writeOptionalString(((IndexFormatTooNewException) throwable).getResourceDescription());
    #             writeInt(((IndexFormatTooNewException) throwable).getVersion());
    #             writeInt(((IndexFormatTooNewException) throwable).getMinVersion());
    #             writeInt(((IndexFormatTooNewException) throwable).getMaxVersion());
    #             writeMessage = false;
    #             writeCause = false;
    #         } else if (throwable instanceof IndexFormatTooOldException) {
    #             writeVInt(3);
    #             IndexFormatTooOldException t = (IndexFormatTooOldException) throwable;
    #             writeOptionalString(t.getResourceDescription());
    #             if (t.getVersion() == null) {
    #                 write_boolean(false);
    #                 writeOptionalString(t.getReason());
    #             } else {
    #                 write_boolean(true);
    #                 writeInt(t.getVersion());
    #                 writeInt(t.getMinVersion());
    #                 writeInt(t.getMaxVersion());
    #             }
    #             writeMessage = false;
    #             writeCause = false;
    #         } else if (throwable instanceof NullPointerException) {
    #             writeVInt(4);
    #             writeCause = false;
    #         } else if (throwable instanceof NumberFormatException) {
    #             writeVInt(5);
    #             writeCause = false;
    #         } else if (throwable instanceof IllegalArgumentException) {
    #             writeVInt(6);
    #         } else if (throwable instanceof AlreadyClosedException) {
    #             writeVInt(7);
    #         } else if (throwable instanceof EOFException) {
    #             writeVInt(8);
    #             writeCause = false;
    #         } else if (throwable instanceof SecurityException) {
    #             writeVInt(9);
    #         } else if (throwable instanceof StringIndexOutOfBoundsException) {
    #             writeVInt(10);
    #             writeCause = false;
    #         } else if (throwable instanceof ArrayIndexOutOfBoundsException) {
    #             writeVInt(11);
    #             writeCause = false;
    #         } else if (throwable instanceof FileNotFoundException) {
    #             writeVInt(12);
    #             writeCause = false;
    #         } else if (throwable instanceof FileSystemException) {
    #             writeVInt(13);
    #             if (throwable instanceof NoSuchFileException) {
    #                 writeVInt(0);
    #             } else if (throwable instanceof NotDirectoryException) {
    #                 writeVInt(1);
    #             } else if (throwable instanceof DirectoryNotEmptyException) {
    #                 writeVInt(2);
    #             } else if (throwable instanceof AtomicMoveNotSupportedException) {
    #                 writeVInt(3);
    #             } else if (throwable instanceof FileAlreadyExistsException) {
    #                 writeVInt(4);
    #             } else if (throwable instanceof AccessDeniedException) {
    #                 writeVInt(5);
    #             } else if (throwable instanceof FileSystemLoopException) {
    #                 writeVInt(6);
    #             } else {
    #                 writeVInt(7);
    #             }
    #             writeOptionalString(((FileSystemException) throwable).getFile());
    #             writeOptionalString(((FileSystemException) throwable).getOtherFile());
    #             writeOptionalString(((FileSystemException) throwable).getReason());
    #             writeCause = false;
    #         } else if (throwable instanceof IllegalStateException) {
    #             writeVInt(14);
    #         } else if (throwable instanceof LockObtainFailedException) {
    #             writeVInt(15);
    #         } else if (throwable instanceof InterruptedException) {
    #             writeVInt(16);
    #             writeCause = false;
    #         } else if (throwable instanceof IOException) {
    #             writeVInt(17);
    #         } else if (throwable instanceof OpenSearchRejectedExecutionException) {
    #             writeVInt(18);
    #             write_boolean(((OpenSearchRejectedExecutionException) throwable).isExecutorShutdown());
    #             writeCause = false;
    #         } else {
    #             final OpenSearchException ex;
    #             if (throwable instanceof OpenSearchException && OpenSearchException.isRegistered(throwable.getClass(), version)) {
    #                 ex = (OpenSearchException) throwable;
    #             } else {
    #                 ex = new NotSerializableExceptionWrapper(throwable);
    #             }
    #             writeVInt(0);
    #             writeVInt(OpenSearchException.getId(ex.getClass()));
    #             ex.writeTo(this);
    #             return;
    #         }
    #         if (writeMessage) {
    #             writeOptionalString(throwable.getMessage());
    #         }
    #         if (writeCause) {
    #             writeException(rootException, throwable.getCause(), nestedLevel + 1);
    #         }
    #         OpenSearchException.writeStackTraces(throwable, this, (o, t) -> o.writeException(rootException, t, nestedLevel + 1));
    #     }
    # }

    # /** Writes the OpenSearch {@link Build} informn to the output stream */
    # def write_build(final Build build) throws IOException {
    #     // the following is new for opensearch: we write the distribution name to support any "forks" of the code
    #     writeString(build.getDistribution());

    #     final Build.Type buildType = build.type();
    #     writeString(buildType.displayName());
    #     writeString(build.hash());
    #     writeString(build.date());
    #     write_boolean(build.isSnapshot());
    #     writeString(build.getQualifiedVersion());
    # }

    # protected boolean failOnTooManyNestedExceptions(Throwable throwable) {
    #     throw new AssertionError("too many nested exceptions", throwable);
    # }

    # /**
    #  Writes a {@link NamedWriteable} to the current stream, by first writing its name and then the object itself
    #  
    # def writeNamedWriteable(NamedWriteable namedWriteable) throws IOException {
    #     writeString(namedWriteable.getWriteableName());
    #     namedWriteable.writeTo(this);
    # }

    # /**
    #  Write an optional {@link NamedWriteable} to the stream.
    #  
    # def writeOptionalNamedWriteable(@Nullable NamedWriteable namedWriteable) throws IOException {
    #     if (namedWriteable == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeNamedWriteable(namedWriteable);
    #     }
    # }

    # /**
    #  Write a {@linkplain ZoneId} to the stream.
    #  
    # def writeZoneId(ZoneId timeZone) throws IOException {
    #     writeString(timeZone.getId());
    # }

    # /**
    #  Write an optional {@linkplain ZoneId} to the stream.
    #  
    # def writeOptionalZoneId(@Nullable ZoneId timeZone) throws IOException {
    #     if (timeZone == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeZoneId(timeZone);
    #     }
    # }

    # /**
    #  Writes a collection to this stream. The corresponding collection can be read from a stream input using
    #  {@link StreamInput#readList(Writeable.Reader)}.
    #      #  @param collection the collection to write to this stream
    #  @throws IOException if an I/O exception occurs writing the collection
    #  
    # def writeCollection(final Collection<? extends Writeable> collection) throws IOException {
    #     writeCollection(collection, (o, v) -> v.writeTo(o));
    # }

    # /**
    #  Writes a list of {@link Writeable} objects
    #  
    # def writeList(List<? extends Writeable> list) throws IOException {
    #     writeCollection(list);
    # }

    # /**
    #  Writes a collection of objects via a {@link Writer}.
    #      #  @param collection the collection of objects
    #  @throws IOException if an I/O exception occurs writing the collection
    #  
    # public <T> void writeCollection(final Collection<T> collection, final Writer<T> writer) throws IOException {
    #     writeVInt(collection.size());
    #     for (final T val : collection) {
    #         writer.write(this, val);
    #     }
    # }

    # /**
    #  Writes a collection of a strings. The corresponding collection can be read from a stream input using
    #  {@link StreamInput#readList(Writeable.Reader)}.
    #      #  @param collection the collection of strings
    #  @throws IOException if an I/O exception occurs writing the collection
    #  
    # def writeStringCollection(final Collection<String> collection) throws IOException {
    #     writeCollection(collection, StreamOutput::writeString);
    # }

    # /**
    #  Writes an optional collection of a strings. The corresponding collection can be read from a stream input using
    #  {@link StreamInput#readList(Writeable.Reader)}.
    #      #  @param collection the collection of strings
    #  @throws IOException if an I/O exception occurs writing the collection
    #  
    # def writeOptionalStringCollection(final Collection<String> collection) throws IOException {
    #     if (collection != null) {
    #         write_boolean(true);
    #         writeCollection(collection, StreamOutput::writeString);
    #     } else {
    #         write_boolean(false);
    #     }
    # }

    # /**
    #  Writes a list of {@link NamedWriteable} objects.
    #  
    # def writeNamedWriteableList(List<? extends NamedWriteable> list) throws IOException {
    #     writeVInt(list.size());
    #     for (NamedWriteable obj : list) {
    #         writeNamedWriteable(obj);
    #     }
    # }

    # /**
    #  Writes an enum with type E based on its ordinal value
    #  
    # public <E extends Enum<E>> void writeEnum(E enumValue) throws IOException {
    #     writeVInt(enumValue.ordinal());
    # }

    # /**
    #  Writes an EnumSet with type E that by serialized it based on it's ordinal value
    #  
    # public <E extends Enum<E>> void writeEnumSet(EnumSet<E> enumSet) throws IOException {
    #     writeVInt(enumSet.size());
    #     for (E e : enumSet) {
    #         writeEnum(e);
    #     }
    # }

    # /**
    #  Write a {@link TimeValue} to the stream
    #  
    # def writeTimeValue(TimeValue timeValue) throws IOException {
    #     writeZLong(timeValue.duration());
    #     write_byte((byte) timeValue.timeUnit().ordinal());
    # }

    # /**
    #  Write an optional {@link TimeValue} to the stream.
    #  
    # def writeOptionalTimeValue(@Nullable TimeValue timeValue) throws IOException {
    #     if (timeValue == null) {
    #         write_boolean(false);
    #     } else {
    #         write_boolean(true);
    #         writeTimeValue(timeValue);
    #     }
    # }
