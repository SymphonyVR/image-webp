# Libwebp-style VP8 coefficient diagnostic

- CPU: `AMD EPYC 9V74 80-Core Processor`
- apply: `0`
- fmt: `0`
- tests: `0`
- clippy: `101`
- MSRV build: `0`

## apply tail
```text
```

## fmt tail
```text
```

## test tail
```text
test alpha_blending::tests::alpha_blending_optimization ... ignored
test decoder::tests::add_with_overflow_size ... ok
test decoder::tests::decode_2x2_single_color_image ... ok
test decoder::tests::decode_3x3_single_color_image ... ok
test extended::tests::binary_alpha_blend_selects_exact_pixel ... ok
test extended::tests::dispose_clear_fullsize_rgb_frame ... ok
test extended::tests::dispose_clear_subframe_rgb_frame ... ok
test extended::tests::reconstruct_alpha_filters ... ok
test lossless::decoder::test::bit_read_error_test ... ok
test lossless::decoder::test::bit_read_test ... ok
test lossy::arithmetic_decoder::tests::test_arithmetic_decoder_hello_long ... ok
test lossy::arithmetic_decoder::tests::test_arithmetic_decoder_hello_short ... ok
test lossy::arithmetic_decoder::tests::test_arithmetic_decoder_uninit ... ok
test lossy::arithmetic_encoder::tests::test_arithmetic_encoder_hello ... ok
test lossy::arithmetic_encoder::tests::test_arithmetic_encoder_short ... ok
test lossy::arithmetic_encoder::tests::test_encoder_tree ... ok
test lossy::arithmetic_encoder::tests::test_encoder_with_decoder ... ok
test lossy::prediction::tests::test_add_residue ... ok
test lossy::prediction::tests::test_avg2 ... ok
test lossy::prediction::tests::test_avg2_specific ... ok
test encoder::tests::write_webp ... ok
test lossy::prediction::tests::test_edge_pixels ... ok
test lossy::prediction::tests::test_predict_bhepred ... ok
test lossy::prediction::tests::test_predict_bldpred ... ok
test lossy::prediction::tests::test_predict_brdpred ... ok
test lossy::prediction::tests::test_predict_bvepred ... ok
test lossy::prediction::tests::test_top_pixels ... ok
test lossy::transform::tests::test_dct_inverse ... ok
test lossy::yuv::tests::test_fancy_grid ... ok
test lossy::yuv::tests::test_yuv_conversions ... ok
test encoder::tests::write_webp_exif ... ok
test encoder::tests::roundtrip_libwebp ... ok
test lossy::prediction::tests::test_avg3 ... ok

test result: ok. 32 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out; finished in 0.62s

[1m[92m     Running[0m `/home/runner/work/image-webp/image-webp/target/debug/deps/decode-c860889ae0ce7648`

running 31 tests
test reftest_animated_random_lossless ... ok
test reftest_animated_random_lossy ... ok
test reftest_gallery1_1 ... ok
test reftest_gallery1_2 ... ok
test reftest_gallery2_1_webp_a ... ok
test reftest_gallery2_1_webp_ll ... ok
test reftest_gallery2_2_webp_a ... ok
test reftest_gallery2_2_webp_ll ... ok
test reftest_gallery1_4 ... ok
test reftest_gallery1_5 ... ok
test reftest_gallery1_3 ... ok
test reftest_gallery2_4_webp_a ... ok
test reftest_gallery2_4_webp_ll ... ok
test reftest_gallery2_5_webp_ll ... ok
test reftest_gallery2_3_webp_ll ... ok
test reftest_gallery2_5_webp_a ... ok
test reftest_gallery2_3_webp_a ... ok
test reftest_nofancy_gallery1_1 ... ok
test reftest_nofancy_gallery1_2 ... ok
test reftest_regression_color_index ... ok
test reftest_regression_dark ... ok
test reftest_regression_lossless_indexed_1bit_palette ... ok
test reftest_regression_lossless_indexed_2bit_palette ... ok
test reftest_regression_lossless_indexed_4bit_palette ... ok
test reftest_regression_tiny ... ok
test test_vp8l_max_height_dimensions ... ok
test test_vp8l_max_width_and_height_dimensions ... ok
test test_vp8l_max_width_dimensions ... ok
test reftest_nofancy_gallery1_5 ... ok
test reftest_nofancy_gallery1_4 ... ok
test reftest_nofancy_gallery1_3 ... ok

test result: ok. 31 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.31s

[1m[92m   Doc-tests[0m image_webp
[1m[92m     Running[0m `/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustdoc --edition=2021 --crate-type lib --color always --crate-name image_webp --test src/lib.rs --test-run-directory /home/runner/work/image-webp/image-webp -L native=/home/runner/work/image-webp/image-webp/target/debug/build/libwebp-sys-7669b733598afc52/out --extern byteorder_lite=/home/runner/work/image-webp/image-webp/target/debug/deps/libbyteorder_lite-a278a9f14042f35b.rlib --extern image_webp=/home/runner/work/image-webp/image-webp/target/debug/deps/libimage_webp-c2294830a6b5f4a4.rlib --extern paste=/home/runner/work/image-webp/image-webp/target/debug/deps/libpaste-594f55fe5cfdc9fd.so --extern png=/home/runner/work/image-webp/image-webp/target/debug/deps/libpng-e598a91edf8375c4.rlib --extern quick_error=/home/runner/work/image-webp/image-webp/target/debug/deps/libquick_error-d88c5aeea3a3d7d1.rlib --extern rand=/home/runner/work/image-webp/image-webp/target/debug/deps/librand-afaa0a85c24cc4e5.rlib --extern webp=/home/runner/work/image-webp/image-webp/target/debug/deps/libwebp-7648140fa8b53cb3.rlib -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps -C embed-bitcode=no --check-cfg 'cfg(docsrs,test)' --check-cfg 'cfg(feature, values("_benchmarks"))' --error-format human`

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

```

## clippy tail
```text
[1m[92m    Checking[0m byteorder-lite v0.1.0
[1m[92m    Checking[0m quick-error v2.0.1
[1m[92m    Checking[0m image-webp v0.2.4 (/home/runner/work/image-webp/image-webp)
[1m[91merror[0m[1m: method `read_sign` is never used[0m
   [1m[94m--> [0msrc/lossy/arithmetic_decoder.rs:185:19
    [1m[94m|[0m
[1m[94m 67[0m [1m[94m|[0m impl ArithmeticDecoder {
    [1m[94m|[0m [1m[94m----------------------[0m [1m[94mmethod in this implementation[0m
[1m[94m...[0m
[1m[94m185[0m [1m[94m|[0m     pub(crate) fn read_sign(&mut self) -> BitResult<bool> {
    [1m[94m|[0m                   [1m[91m^^^^^^^^^[0m
    [1m[94m|[0m
    [1m[94m= [0m[1mnote[0m: `-D dead-code` implied by `-D warnings`
    [1m[94m= [0m[1mhelp[0m: to override `-D warnings` add `#[expect(dead_code)]` or `#[allow(dead_code)]`

[1m[91merror[0m[1m: method `read_sign` is never used[0m
   [1m[94m--> [0msrc/lossy/arithmetic_decoder.rs:505:8
    [1m[94m|[0m
[1m[94m483[0m [1m[94m|[0m impl FastDecoder<'_> {
    [1m[94m|[0m [1m[94m--------------------[0m [1m[94mmethod in this implementation[0m
[1m[94m...[0m
[1m[94m505[0m [1m[94m|[0m     fn read_sign(mut self) -> Option<bool> {
    [1m[94m|[0m        [1m[91m^^^^^^^^^[0m

[1m[91merror[0m: could not compile `image-webp` (lib) due to 2 previous errors
```

## msrv tail
```text
[1m[32m    Updating[0m crates.io index
[1m[32m Downloading[0m crates ...
[1m[32m  Downloaded[0m byteorder-lite v0.1.0
[1m[32m  Downloaded[0m quick-error v2.0.1
[1m[32m   Compiling[0m quick-error v2.0.1
[1m[32m   Compiling[0m byteorder-lite v0.1.0
[1m[32m     Running[0m `/home/runner/.rustup/toolchains/1.80.1-x86_64-unknown-linux-gnu/bin/rustc --crate-name quick_error --edition=2018 /home/runner/.cargo/registry/src/index.crates.io-6f17d22bba15001f/quick-error-2.0.1/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --check-cfg 'cfg(docsrs)' --check-cfg 'cfg(feature, values())' -C metadata=05f97fef35249ec6 -C extra-filename=-05f97fef35249ec6 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --cap-lints allow`
[1m[32m     Running[0m `/home/runner/.rustup/toolchains/1.80.1-x86_64-unknown-linux-gnu/bin/rustc --crate-name byteorder_lite --edition=2021 /home/runner/.cargo/registry/src/index.crates.io-6f17d22bba15001f/byteorder-lite-0.1.0/src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --cfg 'feature="default"' --cfg 'feature="std"' --check-cfg 'cfg(docsrs)' --check-cfg 'cfg(feature, values("default", "std"))' -C metadata=225adb4ca8161e46 -C extra-filename=-225adb4ca8161e46 --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --cap-lints allow`
[1m[32m   Compiling[0m image-webp v0.2.4 (/home/runner/work/image-webp/image-webp)
[1m[32m     Running[0m `/home/runner/.rustup/toolchains/1.80.1-x86_64-unknown-linux-gnu/bin/rustc --crate-name image_webp --edition=2021 src/lib.rs --error-format=json --json=diagnostic-rendered-ansi,artifacts,future-incompat --crate-type lib --emit=dep-info,metadata,link -C embed-bitcode=no -C debuginfo=2 --check-cfg 'cfg(docsrs)' --check-cfg 'cfg(feature, values("_benchmarks"))' -C metadata=57893f2a5355531b -C extra-filename=-57893f2a5355531b --out-dir /home/runner/work/image-webp/image-webp/target/debug/deps -L dependency=/home/runner/work/image-webp/image-webp/target/debug/deps --extern byteorder_lite=/home/runner/work/image-webp/image-webp/target/debug/deps/libbyteorder_lite-225adb4ca8161e46.rmeta --extern quick_error=/home/runner/work/image-webp/image-webp/target/debug/deps/libquick_error-05f97fef35249ec6.rmeta`
[0m[1m[33mwarning[0m[0m[1m: method `read_sign` is never used[0m
[0m   [0m[0m[1m[38;5;12m--> [0m[0msrc/lossy/arithmetic_decoder.rs:185:19[0m
[0m    [0m[0m[1m[38;5;12m|[0m
[0m[1m[38;5;12m67[0m[0m  [0m[0m[1m[38;5;12m|[0m[0m [0m[0mimpl ArithmeticDecoder {[0m
[0m    [0m[0m[1m[38;5;12m|[0m[0m [0m[0m[1m[38;5;12m----------------------[0m[0m [0m[0m[1m[38;5;12mmethod in this implementation[0m
[0m[1m[38;5;12m...[0m
[0m[1m[38;5;12m185[0m[0m [0m[0m[1m[38;5;12m|[0m[0m [0m[0m    pub(crate) fn read_sign(&mut self) -> BitResult<bool> {[0m
[0m    [0m[0m[1m[38;5;12m|[0m[0m                   [0m[0m[1m[33m^^^^^^^^^[0m
[0m    [0m[0m[1m[38;5;12m|[0m
[0m    [0m[0m[1m[38;5;12m= [0m[0m[1mnote[0m[0m: `#[warn(dead_code)]` on by default[0m

[0m[1m[33mwarning[0m[0m[1m: method `read_sign` is never used[0m
[0m   [0m[0m[1m[38;5;12m--> [0m[0msrc/lossy/arithmetic_decoder.rs:505:8[0m
[0m    [0m[0m[1m[38;5;12m|[0m
[0m[1m[38;5;12m483[0m[0m [0m[0m[1m[38;5;12m|[0m[0m [0m[0mimpl FastDecoder<'_> {[0m
[0m    [0m[0m[1m[38;5;12m|[0m[0m [0m[0m[1m[38;5;12m--------------------[0m[0m [0m[0m[1m[38;5;12mmethod in this implementation[0m
[0m[1m[38;5;12m...[0m
[0m[1m[38;5;12m505[0m[0m [0m[0m[1m[38;5;12m|[0m[0m [0m[0m    fn read_sign(mut self) -> Option<bool> {[0m
[0m    [0m[0m[1m[38;5;12m|[0m[0m        [0m[0m[1m[33m^^^^^^^^^[0m

[1m[33mwarning[0m[1m:[0m `image-webp` (lib) generated 2 warnings
[1m[32m    Finished[0m `dev` profile [unoptimized + debuginfo] target(s) in 1.21s
```
